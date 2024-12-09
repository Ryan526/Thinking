# Thinking Indicator Filter

The Thinking Indicator Filter enhances the user experience by adding a visual "Thinking..." indicator during the API processing phase. Once processing is complete, the total elapsed thinking time is displayed in seconds.

## Features

- Displays a "Thinking..." status while waiting for the API response.
- Shows the total elapsed time in seconds after completion (e.g., "Thought for 15 seconds").
- Lightweight and easy to use.

## How It Works

1. **Thinking Indicator**: The filter emits a `Thinking...` status message whenever the API begins processing a response.
2. **Elapsed Time Display**: Once processing concludes, the filter calculates and displays the total time spent (in seconds). For example:
    - `Thought for 15 seconds`.

## Example Output

- During processing:
    ```
    Thinking...
    ```
- After the response is processed:
    ```
    Thought for 15 seconds
    ```
