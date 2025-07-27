from url import URL


if __name__ == "__main__":
    import sys

    brw = URL(sys.argv[1])
    brw.load()

