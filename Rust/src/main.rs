use std::io::{stdin, stdout, Write};

type Board<'a> = [[Option<&'a str>; 3]; 3];

fn print_board(board: &Board) {
    print!("\x1B[2J\x1B[1;1H"); // Clear terminal
    println!("┌───┬───┬───┐");

    let mut counter = 1;

    for (i, row) in board.iter().enumerate() {
        print!("│ ");
        for item in row.iter() {
            match item {
                Some(ch) => print!("{}", &ch),
                None => print!("\x1B[90;3m{}\x1B[0m", counter),
            };
            print!(" │ ");
            counter += 1;
        }

        println!();
        if i < board.len() - 1 {
            println!("├───┼───┼───┤");
        }
    }
    println!("└───┴───┴───┘");
}

fn main() {
    let mut turn = 0;
    let mut symbols = ["\x1B[35mX\x1B[0m", "\x1B[36mO\x1B[0m"].iter().cycle();
    let mut board: Board = Default::default();

    print_board(&board);

    let running = true;
    while running {
        let mut choice: i32;

        loop {
            print!("Choose cell: ");
            stdout().flush().expect("Error");

            let mut input = String::new();
            stdin().read_line(&mut input).expect("Error");

            match input.trim().parse::<i32>() {
                Ok(num) if (1..=9).contains(&num) => {
                    choice = num;
                    break;
                }
                _ => println!("Please choose a number between 1 and 9."),
            }
        }

        let (row, col) = ((choice - 1) / 3, (choice - 1) % 3);
        if board[row as usize][col as usize] != None {
            continue;
        }

        turn += 1;
        let symbol = symbols.next().unwrap();
        board[row as usize][col as usize] = Some(symbol);
        print_board(&board);
    }
}
