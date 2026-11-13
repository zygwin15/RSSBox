from unittest.mock import patch
from django.test import SimpleTestCase
from scripts import personal_init


class PersonalStartupTests(SimpleTestCase):
    def test_only_committed_migrations_are_run(self):
        with (
            patch.object(personal_init.django, "setup"),
            patch.object(personal_init, "call_command") as command,
            patch.object(personal_init, "create_superuser") as create,
        ):
            personal_init.main()
        self.assertEqual(
            [call.args[0] for call in command.call_args_list],
            ["migrate", "collectstatic", "compilemessages"],
        )
        create.assert_called_once()

    def test_migration_failure_aborts_initialization(self):
        with (
            patch.object(personal_init.django, "setup"),
            patch.object(
                personal_init,
                "call_command",
                side_effect=RuntimeError("migration failed"),
            ) as command,
            patch.object(personal_init, "create_superuser") as create,
        ):
            with self.assertRaisesRegex(RuntimeError, "migration failed"):
                personal_init.main()
        self.assertEqual(command.call_count, 1)
        create.assert_not_called()
