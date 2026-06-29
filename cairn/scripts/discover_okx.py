from cairn.brokers.okx.discovery import OKXDiscovery


def main():
    discovery = OKXDiscovery()

    discovery.print_discovery(
        limit=20,
        show_raw_sample=False,
    )

    print("\n===== PAGINATION TEST =====")
    discovery.test_pagination()

    traders = discovery.fetch_pages(pages=5, limit=20)

    print("\nFIRST:", traders[0].get("nickName"))
    print("LAST:", traders[-1].get("nickName"))
if __name__ == "__main__":
    main()