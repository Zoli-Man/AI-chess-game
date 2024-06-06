# Chess AI Game

## Description

This project implements a chess game where a user can play against an AI. The AI is implemented using Rust, with the core logic interfacing with Python via the `pyo3` crate. This combination allows for a powerful and efficient AI integrated with a Python-based interface.

## Features

- **AI Opponent**: Play against a computer-controlled AI with various difficulty levels.
- **User Interface**: Simple Python-based interface for interacting with the game.
- **Efficiency**: Utilizes Rust for the AI logic to ensure fast and efficient performance.
- **Integration**: Seamless integration between Rust and Python using the `pyo3` crate.

## Files

- `lib.rs`: The Rust source code implementing the core logic of the chess AI.
- `test.py`: A Python script for testing the chess AI integration.

## Installation

### Prerequisites

- Rust and Cargo installed
- Python 3.x installed
- `pyo3` crate for Rust
- `maturin` for building and packaging the Rust extension

### Steps

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_name>
```

bash
Build the Rust extension using maturin:

```bash
maturin develop
```

This command will build the Rust extension and install it locally in your Python environment.

3.Run the test script to ensure everything is working:

```bash
python test.py
```

# Usage

Once the installation is complete, you can use the chess AI via the Python interface. Below is an example of how to interact with the AI in a Python script:
