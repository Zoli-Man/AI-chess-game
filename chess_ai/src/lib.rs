use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
enum PieceType {
    R,
    N,
    B,
    Q,
    K,
    P,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
enum Color {
    White,
    Black,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ChessPiece {
    piece_type: PieceType,
    color: Color,
    position: (i32, i32),
    move_count: i32,
    pawn_double_move_at_turn: Option<i32>,
}

impl ChessPiece {
    fn new(piece_type: PieceType, color: Color, position: (i32, i32)) -> Self {
        ChessPiece {
            piece_type,
            color,
            position,
            move_count: 0,
            pawn_double_move_at_turn: None,
        }
    }

    fn move_piece(&mut self, new_position: (i32, i32)) {
        self.position = new_position;
        self.move_count += 1;
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct BoardState {
    pieces: HashMap<(i32, i32), ChessPiece>,
    turn: Color,
    turn_count: i32,
    black_locations: Vec<(i32, i32)>,
    white_locations: Vec<(i32, i32)>,
}

impl BoardState {
    fn new() -> Self {
        let mut pieces = HashMap::new();

        pieces.insert((0, 0), ChessPiece::new(PieceType::R, Color::Black, (0, 0)));
        pieces.insert((0, 1), ChessPiece::new(PieceType::N, Color::Black, (0, 1)));
        pieces.insert((0, 2), ChessPiece::new(PieceType::B, Color::Black, (0, 2)));
        pieces.insert((0, 3), ChessPiece::new(PieceType::Q, Color::Black, (0, 3)));
        pieces.insert((0, 4), ChessPiece::new(PieceType::K, Color::Black, (0, 4)));
        pieces.insert((0, 5), ChessPiece::new(PieceType::B, Color::Black, (0, 5)));
        pieces.insert((0, 6), ChessPiece::new(PieceType::N, Color::Black, (0, 6)));
        pieces.insert((0, 7), ChessPiece::new(PieceType::R, Color::Black, (0, 7)));

        for i in 0..8 {
            pieces.insert((1, i), ChessPiece::new(PieceType::P, Color::Black, (1, i)));
            pieces.insert((6, i), ChessPiece::new(PieceType::P, Color::White, (6, i)));
        }

        pieces.insert((7, 0), ChessPiece::new(PieceType::R, Color::White, (7, 0)));
        pieces.insert((7, 1), ChessPiece::new(PieceType::N, Color::White, (7, 1)));
        pieces.insert((7, 2), ChessPiece::new(PieceType::B, Color::White, (7, 2)));
        pieces.insert((7, 3), ChessPiece::new(PieceType::Q, Color::White, (7, 3)));
        pieces.insert((7, 4), ChessPiece::new(PieceType::K, Color::White, (7, 4)));
        pieces.insert((7, 5), ChessPiece::new(PieceType::B, Color::White, (7, 5)));
        pieces.insert((7, 6), ChessPiece::new(PieceType::N, Color::White, (7, 6)));
        pieces.insert((7, 7), ChessPiece::new(PieceType::R, Color::White, (7, 7)));

        let black_locations = pieces
            .iter()
            .filter(|&(_, v)| v.color == Color::Black)
            .map(|(&k, _)| k)
            .collect();
        let white_locations = pieces
            .iter()
            .filter(|&(_, v)| v.color == Color::White)
            .map(|(&k, _)| k)
            .collect();

        BoardState {
            pieces,
            turn: Color::White,
            turn_count: 0,
            black_locations,
            white_locations,
        }
    }
    fn get_board_as_string(&self) -> String {
        let mut board = String::new();
        for i in 0..8 {
            for j in 0..8 {
                let piece = self.get_piece((i, j));
                match piece {
                    Some(piece) => {
                        let piece_char = match piece.piece_type {
                            PieceType::R => 'r',
                            PieceType::N => 'n',
                            PieceType::B => 'b',
                            PieceType::Q => 'q',
                            PieceType::K => 'k',
                            PieceType::P => 'p',
                        };
                        let color_char = match piece.color {
                            Color::White => piece_char.to_ascii_uppercase(),
                            Color::Black => piece_char,
                        };
                        board.push(color_char);
                    }
                    None => {
                        board.push('.');
                    }
                }
            }
            board.push('\n');
        }
        board
    }
    fn get_piece(&self, position: (i32, i32)) -> Option<&ChessPiece> {
        self.pieces.get(&position)
    }

    fn move_piece(&mut self, start: (i32, i32), end: (i32, i32)) {
        if let Some(mut piece) = self.pieces.remove(&start) {
            let move_is_castling = piece.piece_type == PieceType::K && (start.1 - end.1).abs() > 1;
            let left_castle: bool = end.1 < start.1;

            if move_is_castling {
                let (rook_start, rook_end) = if left_castle {
                    ((start.0, 0), (start.0, 3))
                } else {
                    ((start.0, 7), (start.0, 5))
                };
                if let Some(mut rook_piece) = self.pieces.remove(&rook_start) {
                    rook_piece.move_piece(rook_end);
                    self.pieces.insert(rook_end, rook_piece);
                }
            }

            piece.move_piece(end);

            if piece.piece_type == PieceType::P {
                // promotion
                if end.0 == 0 || end.0 == 7 {
                    piece.piece_type = PieceType::Q;
                }
                if (start.0 - end.0).abs() == 2 {
                    piece.pawn_double_move_at_turn = Some(self.turn_count);
                }
                // en passant
                if end.1 != start.1 && self.get_piece(end).is_none() {
                    let captured_pos = if piece.color == Color::White {
                        (end.0 + 1, end.1)
                    } else {
                        (end.0 - 1, end.1)
                    };
                    self.pieces.remove(&captured_pos);
                }
            }
            let is_capture = self.get_piece(end).is_some();

            if piece.color == Color::Black {
                self.black_locations.retain(|&loc| loc != start);
                self.black_locations.push(end);
                if is_capture {
                    self.white_locations.retain(|&loc| loc != end);
                }
                if move_is_castling {
                    if left_castle {
                        self.black_locations.retain(|&loc| loc != (start.0, 0));
                        self.black_locations.push((start.0, 3));
                    } else {
                        self.black_locations.retain(|&loc| loc != (start.0, 7));
                        self.black_locations.push((start.0, 5));
                    }
                }
            } else {
                self.white_locations.retain(|&loc| loc != start);
                self.white_locations.push(end);
                if is_capture {
                    self.black_locations.retain(|&loc| loc != end);
                }
                if move_is_castling {
                    if left_castle {
                        self.white_locations.retain(|&loc| loc != (start.0, 0));
                        self.white_locations.push((start.0, 3));
                    } else {
                        self.white_locations.retain(|&loc| loc != (start.0, 7));
                        self.white_locations.push((start.0, 5));
                    }
                }
            }

            self.pieces.insert(end, piece);
            self.turn = if self.turn == Color::White {
                Color::Black
            } else {
                Color::White
            };
            self.turn_count += 1;
        }
    }

    fn create_child_board(&self, start: (i32, i32), end: (i32, i32)) -> BoardState {
        let mut new_dict = HashMap::new();
        for (&k, v) in &self.pieces {
            new_dict.insert(k, v.clone());
        }
        let new_turn = self.turn.clone();
        let new_turn_count = self.turn_count;
        let new_black_locations = self.black_locations.clone();
        let new_white_locations = self.white_locations.clone();

        let mut new_board = BoardState {
            pieces: new_dict,
            turn: new_turn,
            turn_count: new_turn_count,
            black_locations: new_black_locations,
            white_locations: new_white_locations,
        };
        new_board.move_piece(start, end);

        new_board
    }

    fn get_all_moves(&self, color: Color) -> Vec<((i32, i32), (i32, i32))> {
        let mut moves = vec![];
        let locations = if color == Color::Black {
            &self.black_locations
        } else {
            &self.white_locations
        };

        for &location in locations {
            moves.extend(self.get_moves_for_piece(location, None));
        }
        moves
    }

    fn get_moves_for_piece(
        &self,
        position: (i32, i32),
        check_test: Option<bool>,
    ) -> Vec<((i32, i32), (i32, i32))> {
        let check_test = check_test.unwrap_or(true);
        let piece = match self.get_piece(position) {
            Some(piece) => piece,
            None => return vec![],
        };

        let mut moves = vec![];

        match piece.piece_type {
            PieceType::P => moves.extend(self.get_pawn_moves(piece)),
            PieceType::N => moves.extend(self.get_knight_moves(piece)),
            PieceType::B => moves.extend(self.get_bishop_moves(piece)),
            PieceType::R => moves.extend(self.get_rook_moves(piece)),
            PieceType::Q => moves.extend(self.get_queen_moves(piece)),
            PieceType::K => moves.extend(self.get_king_moves(piece)),
        };

        // Filter out moves that would put the king in check
        if check_test {
            moves.retain(|&(start, end)| {
                let new_board = self.create_child_board(start, end);
                !new_board.is_king_in_check(piece.color)
            });
        }

        moves
    }

    fn is_king_in_check(&self, color: Color) -> bool {
        let king_pos = self.get_king_position(color);
        let enemy_color = if color == Color::White {
            Color::Black
        } else {
            Color::White
        };

        // iterate over the pieces hashmap and check if any of the enemy pieces can attack the king
        for (_, piece) in &self.pieces {
            if piece.color == enemy_color {
                let moves = self.get_moves_for_piece(piece.position, Some(false));
                for (_, new_pos) in moves {
                    if new_pos == king_pos {
                        return true;
                    }
                }
            }
        }

        false
    }
    fn get_king_position(&self, color: Color) -> (i32, i32) {
        for (_, piece) in &self.pieces {
            if piece.piece_type == PieceType::K && piece.color == color {
                return piece.position;
            }
        }
        let x = self.get_board_as_string();
        println!("turn count: {:?}", self.turn_count);
        println!("turn: {:?}", self.turn);
        println!("board: {:?}", x);
        panic!("King not found");
    }

    fn get_king_moves(&self, piece: &ChessPiece) -> Vec<((i32, i32), (i32, i32))> {
        let mut moves = vec![];
        let (x, y) = piece.position;

        for i in -1..=1 {
            for j in -1..=1 {
                if i != 0 || j != 0 {
                    let new_pos = (x + i, y + j);
                    if self.is_valid_move(piece, new_pos) {
                        moves.push((piece.position, new_pos));
                    }
                }
            }
        }

        if piece.move_count == 0 {
            if piece.color == Color::White {
                if self.can_castle((7, 4), (7, 0)) {
                    moves.push((piece.position, (7, 2)));
                }
                if self.can_castle((7, 4), (7, 7)) {
                    moves.push((piece.position, (7, 6)));
                }
            } else {
                if self.can_castle((0, 4), (0, 0)) {
                    moves.push((piece.position, (0, 2)));
                }
                if self.can_castle((0, 4), (0, 7)) {
                    moves.push((piece.position, (0, 6)));
                }
            }
        }

        moves
    }

    fn can_castle(&self, king_pos: (i32, i32), rook_pos: (i32, i32)) -> bool {
        let (king_x, king_y) = king_pos;
        let (rook_x, rook_y) = rook_pos;

        if king_y > rook_y {
            for y in rook_y + 1..king_y {
                if self.pieces.contains_key(&(king_x, y)) {
                    return false;
                }
            }
        } else {
            for y in king_y + 1..rook_y {
                if self.pieces.contains_key(&(king_x, y)) {
                    return false;
                }
            }
        }

        if let Some(rook_piece) = self.pieces.get(&rook_pos) {
            if rook_piece.piece_type == PieceType::R && rook_piece.move_count == 0 {
                true
            } else {
                false
            }
        } else {
            false
        }
    }

    fn get_queen_moves(&self, piece: &ChessPiece) -> Vec<((i32, i32), (i32, i32))> {
        let mut moves = self.get_bishop_moves(piece);
        moves.extend(self.get_rook_moves(piece));
        moves
    }

    fn get_rook_moves(&self, piece: &ChessPiece) -> Vec<((i32, i32), (i32, i32))> {
        let mut moves = vec![];
        let (x, y) = piece.position;

        for i in (0..x).rev() {
            if self.is_valid_move(piece, (i, y)) {
                moves.push((piece.position, (i, y)));
            }
            if self.pieces.contains_key(&(i, y)) {
                break;
            }
        }
        for i in x + 1..8 {
            if self.is_valid_move(piece, (i, y)) {
                moves.push((piece.position, (i, y)));
            }
            if self.pieces.contains_key(&(i, y)) {
                break;
            }
        }
        for j in (0..y).rev() {
            if self.is_valid_move(piece, (x, j)) {
                moves.push((piece.position, (x, j)));
            }
            if self.pieces.contains_key(&(x, j)) {
                break;
            }
        }
        for j in y + 1..8 {
            if self.is_valid_move(piece, (x, j)) {
                moves.push((piece.position, (x, j)));
            }
            if self.pieces.contains_key(&(x, j)) {
                break;
            }
        }

        moves
    }

    fn get_bishop_moves(&self, piece: &ChessPiece) -> Vec<((i32, i32), (i32, i32))> {
        let mut moves = vec![];
        let (x, y) = piece.position;

        for i in 1..8 {
            if x + i < 8 && y + i < 8 {
                if self.is_valid_move(piece, (x + i, y + i)) {
                    moves.push((piece.position, (x + i, y + i)));
                }
                if self.pieces.contains_key(&(x + i, y + i)) {
                    break;
                }
            }
        }
        for i in 1..8 {
            if x + i < 8 && y >= i {
                if self.is_valid_move(piece, (x + i, y - i)) {
                    moves.push((piece.position, (x + i, y - i)));
                }
                if self.pieces.contains_key(&(x + i, y - i)) {
                    break;
                }
            }
        }
        for i in 1..8 {
            if x >= i && y + i < 8 {
                if self.is_valid_move(piece, (x - i, y + i)) {
                    moves.push((piece.position, (x - i, y + i)));
                }
                if self.pieces.contains_key(&(x - i, y + i)) {
                    break;
                }
            }
        }
        for i in 1..8 {
            if x >= i && y >= i {
                if self.is_valid_move(piece, (x - i, y - i)) {
                    moves.push((piece.position, (x - i, y - i)));
                }
                if self.pieces.contains_key(&(x - i, y - i)) {
                    break;
                }
            }
        }

        moves
    }

    fn get_knight_moves(&self, piece: &ChessPiece) -> Vec<((i32, i32), (i32, i32))> {
        let mut moves = vec![];
        let (x, y) = piece.position;
        let knight_moves = [
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
        ];

        for (dx, dy) in &knight_moves {
            let new_pos = (x + dx, y + dy);
            if self.is_valid_move(piece, new_pos) {
                moves.push((piece.position, new_pos));
            }
        }

        moves
    }

    fn get_pawn_moves(&self, piece: &ChessPiece) -> Vec<((i32, i32), (i32, i32))> {
        let mut moves = vec![];
        let (x, y) = piece.position;
        let direction = if piece.color == Color::White { -1 } else { 1 };
        let start_row = if piece.color == Color::White { 6 } else { 1 };

        let forward_one = (x + direction, y);
        if !self.pieces.contains_key(&forward_one) {
            moves.push((piece.position, forward_one));
            let forward_two = (x + 2 * direction, y);
            if x == start_row && !self.pieces.contains_key(&forward_two) {
                moves.push((piece.position, forward_two));
            }
        }

        let captures = [(x + direction, y - 1), (x + direction, y + 1)];
        for &capture in &captures {
            if self.is_valid_move(piece, capture)
                && self.pieces.contains_key(&capture)
                && self.pieces[&capture].color != piece.color
            {
                moves.push((piece.position, capture));
            }
        }

        let en_passant_row = if piece.color == Color::White { 3 } else { 4 };
        if x == en_passant_row {
            //println!("en passant row");
            let left = (x, y - 1);
            let right = (x, y + 1);

            if let Some(left_piece) = self.pieces.get(&left) {
                /*println!("left piece: {:?}", left_piece);
                println!("left piece color: {:?}", left_piece.color);
                println!("left piece move count: {:?}", left_piece.move_count);
                println!(
                    "left piece pawn double move at turn: {:?}",
                    left_piece.pawn_double_move_at_turn
                );*/
                //println!("self move count: {:?}", self.turn_count);
                if left_piece.piece_type == PieceType::P
                    && left_piece.color != piece.color
                    && left_piece.move_count == 1
                    && left_piece.pawn_double_move_at_turn == Some(self.turn_count - 1)
                {
                    moves.push((piece.position, (x + direction, y - 1)));
                }
            }
            if let Some(right_piece) = self.pieces.get(&right) {
                if right_piece.piece_type == PieceType::P
                    && right_piece.color != piece.color
                    && right_piece.move_count == 1
                    && right_piece.pawn_double_move_at_turn == Some(self.turn_count - 1)
                {
                    moves.push((piece.position, (x + direction, y + 1)));
                }
            }
        }

        moves
    }

    fn is_valid_move(&self, piece: &ChessPiece, new_position: (i32, i32)) -> bool {
        if new_position.0 < 0 || new_position.0 >= 8 || new_position.1 < 0 || new_position.1 >= 8 {
            return false;
        }

        match self.get_piece(new_position) {
            Some(target_piece) => target_piece.color != piece.color,
            None => true,
        }
    }
    fn minimax(&self, depth: i32, mut alpha: i32, mut beta: i32, maximizing_player: bool) -> i32 {
        if depth == 0 {
            return self.evaluate_board();
        }

        if maximizing_player {
            //println!("MAXX player, depth: {:?}", depth);
            // black is the maximizing player
            let moves = self.get_all_moves(Color::Black);
            let mut max_eval = std::i32::MIN;
            for &(start, end) in &moves {
                let new_board = self.create_child_board(start, end);
                let eval = new_board.minimax(depth - 1, alpha, beta, false);
                max_eval = max_eval.max(eval);
                alpha = alpha.max(eval);
                if beta <= alpha {
                    break;
                }
            }
            max_eval
        } else {
            //println!("MINNN player, depth: {:?}", depth);
            // white is the minimizing player
            let moves: Vec<((i32, i32), (i32, i32))> = self.get_all_moves(Color::White);
            let mut min_eval = std::i32::MAX;
            for &(start, end) in &moves {
                let new_board = self.create_child_board(start, end);
                let eval = new_board.minimax(depth - 1, alpha, beta, true);
                min_eval = min_eval.min(eval);
                beta = beta.min(eval);
                if beta <= alpha {
                    break;
                }
            }
            min_eval
        }
    }
    fn is_it_checkmate(&self, color: Color) -> bool {
        let moves = self.get_all_moves(color);
        moves.is_empty()
    }

    fn evaluate_board(&self) -> i32 {
        let mut score = 0;
        /*if self.is_it_checkmate(Color::White) {
            score = std::i32::MIN;
            return score;
        } else if self.is_it_checkmate(Color::Black) {
            score = std::i32::MAX;
            return score;
        }*/
        for (_, piece) in &self.pieces {
            let piece_value = match piece.piece_type {
                PieceType::P => 1,
                PieceType::N => 3,
                PieceType::B => 3,
                PieceType::R => 5,
                PieceType::Q => 9,
                PieceType::K => 1000,
            };
            let color_value = if piece.color == Color::White { -1 } else { 1 };
            score += piece_value * color_value;
        }
        score
    }
}

#[pyclass]
struct PyBoardState {
    board_state: BoardState,
}

#[pymethods]
impl PyBoardState {
    #[new]
    fn new() -> Self {
        PyBoardState {
            board_state: BoardState::new(),
        }
    }

    fn move_piece(&mut self, start: (i32, i32), end: (i32, i32)) {
        self.board_state.move_piece(start, end);
    }

    fn get_turn(&self) -> i8 {
        match self.board_state.turn {
            Color::White => 0,
            Color::Black => 1,
        }
    }
    fn get_move_for_location(&self, location: (i32, i32)) -> Vec<((i32, i32), (i32, i32))> {
        self.board_state.get_moves_for_piece(location, None)
    }

    fn get_all_moves(&self, color_index: i8) -> Vec<((i32, i32), (i32, i32))> {
        let color = if color_index == 0 {
            Color::White
        } else {
            Color::Black
        };
        self.board_state.get_all_moves(color)
    }
    // low case for black, upper case for white
    fn get_board_as_string(&self) -> String {
        self.board_state.get_board_as_string()
    }
    fn get_best_move(&self) -> ((i32, i32), (i32, i32)) {
        let mut best_move = ((-1, -1), (-1, -1));
        let mut best_score = std::i32::MIN;
        //let color = Color::Black; // black is the maximizing player

        let moves = self.board_state.get_all_moves(Color::Black);
        for &(start, end) in &moves {
            /*test
            let mut x = self.board_state.pieces.get(&start).unwrap();
            let mut y = x.clone();
            y.move_piece(end);
            println!("test: {:?}", x);
            println!("test: {:?}", y);
            return ((-1, -1), (-1, -1));

            //end test*/
            let new_board = self.board_state.create_child_board(start, end);
            //let max_player = color == Color::Black; // black is the maximizing player
            let score = new_board.minimax(3, std::i32::MIN, std::i32::MAX, false);
            if score > best_score {
                best_score = score;
                best_move = (start, end);
            }
        }
        println!("best score: {:?}", best_score);
        println!("best move: {:?}", best_move);
        best_move
    }
}

#[pymodule]
fn chess_ai(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyBoardState>()?;
    Ok(())
}
