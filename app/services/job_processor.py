class JobProcessor:
    """Builds the final text sent to a future AI integration."""

    @staticmethod
    def build_input(ai_prompt: str, job_description: str, latex_resume: str) -> str:
        return (
            f"{ai_prompt.strip()}\n\n"
            "## JOB DESCRIPTION Below\n\n"
            f"{job_description.strip()}\n\n"
            "## RESUME LaTeX code Below\n\n"
            f"{latex_resume.strip()}"
        )
