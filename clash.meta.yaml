port: 7890
socks-port: 7891
allow-lan: true
external-controller: ':9090'
global-client-fingerprint: chrome
log-level: info
mode: script
script:
  enable: true
  path: ./scripts/main.js
mitm:
  enable: true
  host:
    - '*.google.com'
    - '*.twitter.com'
    - 'api.example.com'
dns:
  enable: true
  listen: 0.0.0.0:1053
  ipv6: false
  use-hosts: true
  enhanced-mode: redir-host
  respect-rules: true
  fake-ip-range: 198.18.0.1/15
  default-nameserver: [223.5.5.5, 119.29.29.29]
  proxy-server-nameserver: [https://223.5.5.5/dns-query]
  nameserver: [https://dns.alidns.com/dns-query, https://doh.pub/dns-query]
  fallback: [https://1.1.1.1/dns-query, https://8.8.8.8/dns-query]
  fallback-filter: { geosite: [cn] }
  nameserver-policy:
    "geosite:cn,apple,category-games@cn": [223.5.5.5, 119.29.29.29]
    "geosite:private": [system]
proxy-providers:
  MySubscription:
    type: http
    url: https://api.immtel.co/?L1N1YnNjcmlwdGlvbi9DbGFzaD90PTIwMjImc2lkPTIyNTE2JnRva2VuPWRmNDZhNmM0NjMyY2U3Jm1tPTMyNjAyJmt0bW09UE5MaiUyZm1kUjlkUkdGbzZhRWdvRndBJTNkJTNkJjlkZTczZjAzYzA1NjQ5OTQ5ZmIzY2NlNmY=
    interval: 3600
    path: ./proxies/sub.yaml
    health-check:
      enable: true
      url: http://www.google.com/generate_204
      interval: 600
proxy-groups:
  - {name: ✈️ Proxies, type: select, use: [MySubscription]}
  - {name: 🎯Direct, type: select, proxies: [DIRECT, ✈️ Proxies]}
  - {name: 🚀 Final, type: select, proxies: [✈️ Proxies, 🎯Direct]}
  - {name: 📺 YouTube, type: select, proxies: [✈️ Proxies, 🎯Direct]}
  - {name: 🎮 Bahamut, type: select, proxies: [✈️ Proxies, 🎯Direct]}
  - {name: 📚 Manga Shelf, type: select, proxies: [✈️ Proxies, 🎯Direct]}
  - {name: 🤖 AI, type: select, proxies: [✈️ Proxies, 🎯Direct]}
  - {name: 📲 Telegram, type: select, proxies: [✈️ Proxies, 🎯Direct]}
  - {name: 🐦 Twitter, type: select, proxies: [✈️ Proxies, 🎯Direct]}
  - {name: 💻 Microsoft, type: select, proxies: [🎯Direct, ✈️ Proxies]}
  - {name: 🍎 Apple, type: select, proxies: [🎯Direct, ✈️ Proxies]}
  - {name: 🌐 Google, type: select, proxies: [✈️ Proxies, 🎯Direct]}
  - {name: 🎵 Tiktok, type: select, proxies: [✈️ Proxies, 🎯Direct]}
rules:
  - MATCH,🚀 Final
