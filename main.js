function main(metadata) {
    const { host, dstIP } = metadata;

    if (isDomain('geosite:google')) return '🌐 Google';
    if (isDomain('geosite:youtube')) return '📺 YouTube';
    if (isDomain('geosite:twitter')) return '🐦 Twitter';
    if (isDomain('geosite:telegram')) return '📲 Telegram';
    if (isDomain('geosite:openai')) return '🤖 AI';
    if (host.endsWith('poe.com')) return '🤖 AI';
    if (isDomain('geosite:bahamut')) return '🎮 Bahamut';
    if (isDomain('geosite:apple')) return '🍎 Apple';
    if (isDomain('geosite:microsoft')) return '💻 Microsoft';
    if (isDomain('geosite:tiktok')) return '🎵 Tiktok';

    if (host.endsWith('manhuagui.com') || host.endsWith('mhgui.com') || host.endsWith('hamreus.com')) {
        return '📚 Manga Shelf';
    }

    if (host.endsWith('sitemaji.com')) {
        return 'REJECT';
    }

    if (dstIP && isPrivate(dstIP)) {
        return '🎯Direct';
    }

    if (dstIP && lookupGEOIP(dstIP) === 'CN') {
        return '🎯Direct';
    }

    return '🚀 Final';
}

function fiddler(session) {
    if (session.request.host.includes('google.com')) {
        session.request.headers['User-Agent'] = ['MyAwesomeMetaClient/1.0'];
    }

    if (session.request.host === 'a.com') {
        session.request.host = 'b.com';
        session.request.headers['Host'] = ['b.com'];
    }

    if (session.request.host.includes('ad-server.com')) {
        session.response = {
            status: 200,
            headers: { 'Content-Type': ['text/plain'] },
            body: new TextEncoder().encode('Blocked by Meta Script')
        };
    }

    return session;
}
