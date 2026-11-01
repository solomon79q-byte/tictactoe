from rich.console import Console
from rich.prompt import Prompt, IntPrompt
import sys

import threading

from .play_with_cpu import play_with_cpu

from .udp import upd_discovery_client, upd_discovery_server
from .client import play
from .server import TCPGameServer
from .two_players import two_players

from .game import Game
console = Console()

console.print("[bold green]Tic-Tac-Toe CLI[/bold green]")

def main_menu():
    console.print("\n[bold]Main Menu[/bold]")
    console.print("1. Play against CPU")
    console.print("2. Play against another player")
    console.print("3. Play over LAN (host)")
    console.print("4. Play over LAN (guest)")
    console.print("5. Exit")

    return Prompt.ask("Choice: ", choices=[str(i) for i in range(1, 6)])
    

def selection(choice):
    if choice == '1':
        cpu()
    elif choice == '2':
        two_player()
    elif choice == '3':
        host()

    elif choice == "4":
        guest()

    elif choice == '5':
        console.print("[bold red]Exiting...[/bold red]")
        return False
    else:
        console.print("[bold red]Invalid choice. Please try again.[/bold red]")
        return None

def cpu():
    name = Prompt.ask("Enter your name: ", default="Player 1")
    difficulty = IntPrompt.ask("Choose difficulty (1-Easy, 2-Medium, 3-Hard): ", choices=["1", "2", "3"])
    computer_letter = "0"
    
    
    play_with_cpu(Game(name, "CPU"), difficulty)


def two_player():
    player1 = Prompt.ask("Player 1 name: ", default="PLayer 1")
    player2 = Prompt.ask("Player 2 name: ", default="Player 2")

    two_players(Game(player1, player2))

def host():
    room_code = Prompt.ask("Enter room code")
    threading.Thread(target=upd_discovery_server, args=(room_code,), daemon=True).start()

    host = '0.0.0.0'
    
    game = Game('Player 1', 'Player 2')

    TCPGameServer(game, host=host, port=54321).serve_forever()

def guest():
    room_code = Prompt.ask("Enter room code")
    addr = upd_discovery_client(room_code)
    play(addr[0], addr[1])

while True:
    quit = selection(main_menu())
    if quit == False:
        sys.exit()