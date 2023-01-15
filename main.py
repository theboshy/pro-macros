import gui
import macro_reader


def main():
    macro_reader.start_listener()
    main_window = gui.create_gui()
    main_window.mainloop()
    macro_reader.stop_and_join_listener()  # join to gui thread


if __name__ == "__main__":
    main()
