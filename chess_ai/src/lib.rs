use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

/// Example function to calculate the best move
#[pyfunction]
fn best_move(
    board_pos: Vec<Vec<i32>>,
    moves_count_piece: Vec<Vec<i32>>,
    double_move: Vec<Vec<i32>>,
    turn_count: i32,
) -> i32 {
    println!("Board Position: {:?}", board_pos);
    println!("Moves Count Piece: {:?}", moves_count_piece);
    println!("Double Move: {:?}", double_move);
    println!("Turn Count: {:?}", turn_count);

    42
}

/// A Python module implemented in Rust.
#[pymodule]
fn chess_ai(py: Python, m: &PyModule) -> PyResult<()> {
    // Add the function to the module
    m.add_function(wrap_pyfunction!(best_move, m)?)?;
    Ok(())
}
