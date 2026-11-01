from rich.prompt import Prompt, IntPrompt



def two_players(game) -> None:
    game.print_board_instructions()

    while True:
        game.console.print(f"\n{game.player1} is [blue]X[/blue]")
        game.console.print(f"{game.player2} is [red]O[/red]")   

        while True:
            game.print_board()
            square = IntPrompt.ask(f"{game.current_player}, choose your move (1-9): ", choices=[str(i) for i in range(1, 10)]) - 1
            letter = 'X' if game.current_player == game.player1 else 'O'

            if game.make_move(square, letter):
                if game.current_winner:
                    game.print_board()
                    game.console.print(f"[green]{game.current_player} wins![/green]")
                    if game.current_player == game.player1:
                        game.player1_wins += 1
                    else:
                        game.player2_wins += 1
                    game.print_scoreboard()
                    break
                elif game.check_full_board():
                    game.print_board()
                    game.console.print("[yellow]It's a tie![/yellow]")
                    game.draws += 1
                    game.print_scoreboard()
                    break
                else:
                    # Switch players
                    game.current_player = game.player2 if game.current_player == game.player1 else game.player1
            else:
                game.console.print("[red]Invalid move. Try again.[/red]")

        if game.replay():
            game.next_play()
        else:
            game.console.print("[red]Exiting...[/red]")
            break
