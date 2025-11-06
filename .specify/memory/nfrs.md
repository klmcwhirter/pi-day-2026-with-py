# Non-Functional Requirements

## Technology Stack

- Python >= 3.14
- uv (cli from $PATH)
- uvextras (cli from $PATH)
- Django >= 5.2
- tailwindcss >= 4.1
- npm (cli from $PATH)

## Technology Principles

* Use typical Python standards and conventions with the following overrides:
  - Prefer single-quote chars over double-quote chars
  - Allow 140 char line lengths

* Use Django standards and conventions
* Prefer tailwindcss utility classes over custom CSS classes

## Testing Principles

- Focus on testing business logic only; discourage UI testing
