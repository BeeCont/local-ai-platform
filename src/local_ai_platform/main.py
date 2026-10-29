"""Main file for launching and setup"""

from local_ai_platform.core.command_runner import run_command
from local_ai_platform.logging_config import configure_logging


def main() -> None:
    """Main entry point for the application."""

    # Configure logging settings
    configure_logging()

    result = run_command(
        ["curl", "-I", "--max-time", "5", "https://www.google.com/"],
        timeout=1,
    )

    print("\n" + "=" * 60)
    print("COMMAND RUNNER — TEST")
    print("=" * 60)

    print(f"Command:          {' '.join(result.command)}")
    print(f"Status:           {result.status.value}")
    print(f"Success:          {result.success}")
    print(f"Return code:      {result.returncode}")
    print(f"Duration:         {result.duration_seconds:.2f} seconds")

    print("-" * 60)
    print(f"Error:            {result.error or 'None'}")

    print("-" * 60)
    print("Standard Output:")
    print(result.stdout.strip() or "(empty)")

    print("-" * 60)
    print("Standard Error:")
    print(result.stderr.strip() or "(empty)")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
