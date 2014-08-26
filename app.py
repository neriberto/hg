import sys

from hg import hg


def main():
    HG = hg(5)
    HG.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    except SystemExit:
        pass
