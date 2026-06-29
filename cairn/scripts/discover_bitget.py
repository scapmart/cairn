from cairn.brokers.bitget.discovery import BitgetDiscovery


def main():
    discovery = BitgetDiscovery()
    discovery.discover()


if __name__ == "__main__":
    main()