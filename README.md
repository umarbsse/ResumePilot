# ResumePilot

ResumePilot is a lightweight Python desktop application for preparing job-specific resume input using saved AI prompts, job descriptions, and LaTeX resume templates.

It is built with **Tkinter** for the desktop interface and **SQLite** for local persistence. No third-party Python packages are required.

## Features

### Settings

ResumePilot provides a Settings page where the following values are saved locally:

- AI Prompt
- Cover Letter Prompt
- User LaTeX Resume Code (International)
- User LaTeX Resume Code (Local)
- Cover letter resume code (International)
- Cover letter resume code (Local)

Click **Save Settings** to persist the values in the local SQLite database.

### Job Apply

The Job Apply page provides an **Add New Job** workflow with:

- AI Prompt loaded from Settings
- Job Description entered by the user
- Resume type selector: Local or International
- User LaTeX Resume Code loaded from the selected saved resume template

When **Process** is pressed, ResumePilot generates the final text in this order:

```text
AI Prompt

Job Description

User LaTeX Resume Code
```

The generated result can be reviewed and copied from the application.

## Local Storage

Application settings are stored in a local SQLite database at:

```text
~/.resumepilot/resumepilot.db
```

The database directory is created automatically when the application starts.

## Project Structure

```text
ResumePilot/
├── main.py
├── README.md
├── .gitignore
└── app/
    ├── __init__.py
    ├── application.py
    ├── config.py
    ├── db/
    │   ├── __init__.py
    │   ├── database.py
    │   └── settings_repository.py
    ├── services/
    │   ├── __init__.py
    │   └── job_processor.py
    └── ui/
        ├── __init__.py
        ├── job_apply_page.py
        ├── main_window.py
        ├── settings_page.py
        └── widgets.py
```

## Requirements

- Python 3.10 or newer recommended
- Tkinter
- SQLite, included with standard Python installations

No external Python packages are required.

## Run ResumePilot

Clone the repository:

```bash
git clone <your-repository-url>
cd ResumePilot
```

Run the application:

```bash
python main.py
```

On some Linux distributions, Tkinter may need to be installed separately. For Debian/Ubuntu:

```bash
sudo apt install python3-tk
```

## Processing Logic

The Process button validates the required Job Apply fields and combines them with blank lines between each section:

1. AI Prompt
2. Job Description
3. Selected User LaTeX Resume Code

Changes made directly on the Job Apply page apply only to the current job. To update persisted defaults, edit them on the Settings page and click **Save Settings**.

## Planned Extensions

The modular structure is suitable for future additions such as:

- AI API integration
- Cover-letter generation
- Job application history
- LaTeX compilation
- PDF resume generation
- Job application tracking

## License

Add the license appropriate for your project before publishing or distributing the repository.

## Generated Output Format

When **Process** is clicked, ResumePilot builds the final string in this exact format:

```text
[Saved AI Prompt]

## JOB DESCRIPTION Below

[Job Description entered by the user]

## RESUME LaTeX code Below

[Selected Local or International LaTeX resume code]
```

