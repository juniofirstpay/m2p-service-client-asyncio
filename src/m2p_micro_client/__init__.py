from .service import configure as configure_http_client, m2p_client_session


async def configure(base_url):
    session = await configure_http_client(base_url)
    m2p_client_session.set(session)

    async def clean():
        await session.close()
        m2p_client_session.set(None)

    return clean()