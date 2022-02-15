## 💬 What is this?
- WireHole is a combination of WireGuard, Pi-Hole, Unbound, and Stubby for secure VPN and DoT (DNS over TLS) in a docker-compose project
- RaSoPle is a combination of Radarr, Sonarr, Lidarr, Jackett, flaresolverr, rdt-client, Plex in a one docker-compose project.
- With the intent of enabling users to quickly and easily create and deploy a personally managed full or split-tunnel WireGuard VPN with ad blocking capabilities (via Pihole), first DNS caching with additional privacy options (via Unbound) and second DoT (DNS over TLS) within Stubby.
- This project can be used for x86-64, arm64 or armhf architecture.
- You can have access to all your Series, Movies, Music, EBook over secure VPN. Note that all services are not publically exposed, the idea is to guarantee the privacy and security.
## 👤 Author
* Twitter: [@belarbi2733](https://twitter.com/belarbi2733)
* Github: [@belarbi2733](https://github.com/belarbi2733)
## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/belarbi2733/wirehole-radarr-sonarr/issues). 

## Show your support

Give a ⭐ if this project helped you!

<a href="https://www.buymeacoffee.com/belarbima" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-orange.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

## 🌉 WireHole
WireHole is a combination of [WireGuard®](https://www.wireguard.com/), [Pi-Hole®](https://en.wikipedia.org/wiki/Pi-hole), [Unbound®](https://en.wikipedia.org/wiki/Unbound_(DNS_server)), and [Stubby®](https://dnsprivacy.org/dns_privacy_daemon_-_stubby/) for secure VPN and [DoT](https://en.wikipedia.org/wiki/DNS_over_TLS) (DNS over TLS) in a docker-compose project
### 💻 Supported Architectures

The Wireguard image supports multiple architectures such as `x86-64`, `arm64` and `armhf`. Linuxserver - who makes the wireguard image we use - utilises the docker manifest for multi-platform awareness. 

**The architectures supported by this image are:**

| Architecture | Tag |
| :----: | --- |
| x86-64 | amd64-latest |
| arm64 | arm64v8-latest |
| armhf | arm32v7-latest |

### 💪 Quickstart
To get started all you need to do is clone the repository and spin up the containers.
```bash
git clone https://github.com/belarbi2733/wirehole-radarr-sonarr
```
```bash
cd wirehole-radarr-sonarr/WireHole
```
```bash
docker-compose up -d
```


## 🙏 Feedback

If you have any feedback, please reach out to us at mohammed@belarbi.online



