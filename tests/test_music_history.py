import asyncio
from unittest.mock import AsyncMock

from yandex_music import ClientAsync, Track


class TestMusicHistory:
    track_id_1 = '12345678'
    track_id_2 = '87654321'
    album_id_1 = '11111111'
    album_id_2 = '22222222'
    artist_id_1 = 1000000
    track_title_1 = 'Track Title 1'
    track_title_2 = 'Track Title 2'
    album_title_1 = 'Album Title 1'
    album_title_2 = 'Album Title 2'
    artist_name_1 = 'Artist Name 1'

    def test_music_history(self):
        mock_response = {
            'history_tabs': [
                {
                    'date': '2026-01-21',
                    'items': [
                        {
                            'context': {'type': 'search'},
                            'tracks': [
                                {
                                    'type': 'track',
                                    'data': {
                                        'item_id': {
                                            'track_id': self.track_id_1,
                                            'album_id': self.album_id_1,
                                        },
                                        'full_model': {
                                            'id': self.track_id_1,
                                            'real_id': self.track_id_1,
                                            'title': self.track_title_1,
                                            'available': True,
                                            'available_for_premium_users': True,
                                            'duration_ms': 156210,
                                            'artists': [
                                                {
                                                    'id': self.artist_id_1,
                                                    'name': self.artist_name_1,
                                                    'various': False,
                                                    'composer': False,
                                                    'available': True,
                                                }
                                            ],
                                            'albums': [
                                                {
                                                    'id': int(self.album_id_1),
                                                    'title': self.album_title_1,
                                                    'meta_type': 'music',
                                                    'year': 2020,
                                                    'available': True,
                                                    'available_for_premium_users': True,
                                                }
                                            ],
                                        },
                                    },
                                },
                                {
                                    'type': 'track',
                                    'data': {
                                        'item_id': {
                                            'track_id': self.track_id_2,
                                            'album_id': self.album_id_2,
                                        },
                                        'full_model': {
                                            'id': self.track_id_2,
                                            'real_id': self.track_id_2,
                                            'title': self.track_title_2,
                                            'available': True,
                                            'available_for_premium_users': True,
                                            'duration_ms': 115000,
                                            'artists': [
                                                {
                                                    'id': self.artist_id_1,
                                                    'name': self.artist_name_1,
                                                    'various': False,
                                                    'composer': False,
                                                    'available': True,
                                                }
                                            ],
                                            'albums': [
                                                {
                                                    'id': int(self.album_id_2),
                                                    'title': self.album_title_2,
                                                    'type': 'single',
                                                    'meta_type': 'music',
                                                    'year': 2019,
                                                    'available': True,
                                                    'available_for_premium_users': True,
                                                }
                                            ],
                                        },
                                    },
                                },
                            ],
                        },
                    ],
                },
            ],
        }

        async def run_test():
            client = ClientAsync(token='test_token')  # noqa: S106
            client.base_url = 'https://api.music.yandex.net'
            client._request = AsyncMock()
            client._request.get = AsyncMock(return_value=mock_response)

            tracks = await client.music_history()

            assert isinstance(tracks, list)
            assert len(tracks) == 2
            assert all(isinstance(track, Track) for track in tracks)
            assert tracks[0].id == self.track_id_1
            assert tracks[0].title == self.track_title_1
            assert tracks[1].id == self.track_id_2
            assert tracks[1].title == self.track_title_2

            client._request.get.assert_called_once()
            call_args = client._request.get.call_args
            assert 'fullModelsCount' in call_args.kwargs.get('params', {})
            assert call_args.kwargs['params']['fullModelsCount'] == 999999999

        asyncio.run(run_test())

    def test_music_history_empty_response(self):
        mock_response = {'history_tabs': []}

        async def run_test():
            client = ClientAsync(token='test_token')  # noqa: S106
            client.base_url = 'https://api.music.yandex.net'
            client._request = AsyncMock()
            client._request.get = AsyncMock(return_value=mock_response)

            tracks = await client.music_history()

            assert isinstance(tracks, list)
            assert len(tracks) == 0

        asyncio.run(run_test())

    def test_music_history_no_tracks(self):
        mock_response = {
            'history_tabs': [
                {
                    'date': '2026-01-21',
                    'items': [
                        {
                            'context': {'type': 'search'},
                            'tracks': [],
                        },
                    ],
                },
            ],
        }

        async def run_test():
            client = ClientAsync(token='test_token')  # noqa: S106
            client.base_url = 'https://api.music.yandex.net'
            client._request = AsyncMock()
            client._request.get = AsyncMock(return_value=mock_response)

            tracks = await client.music_history()

            assert isinstance(tracks, list)
            assert len(tracks) == 0

        asyncio.run(run_test())

    def test_music_history_multiple_tabs(self):
        mock_response = {
            'history_tabs': [
                {
                    'date': '2026-01-21',
                    'items': [
                        {
                            'context': {'type': 'search'},
                            'tracks': [
                                {
                                    'type': 'track',
                                    'data': {
                                        'full_model': {
                                            'id': self.track_id_1,
                                            'title': self.track_title_1,
                                            'available': True,
                                            'available_for_premium_users': True,
                                            'duration_ms': 156210,
                                            'artists': [],
                                            'albums': [],
                                        },
                                    },
                                },
                            ],
                        },
                    ],
                },
                {
                    'date': '2026-01-20',
                    'items': [
                        {
                            'context': {'type': 'wave'},
                            'tracks': [
                                {
                                    'type': 'track',
                                    'data': {
                                        'full_model': {
                                            'id': self.track_id_2,
                                            'title': self.track_title_2,
                                            'available': True,
                                            'available_for_premium_users': True,
                                            'duration_ms': 115000,
                                            'artists': [],
                                            'albums': [],
                                        },
                                    },
                                },
                            ],
                        },
                    ],
                },
            ],
        }

        async def run_test():
            client = ClientAsync(token='test_token')  # noqa: S106
            client.base_url = 'https://api.music.yandex.net'
            client._request = AsyncMock()
            client._request.get = AsyncMock(return_value=mock_response)

            tracks = await client.music_history()

            assert isinstance(tracks, list)
            assert len(tracks) == 2
            assert all(isinstance(track, Track) for track in tracks)
            assert tracks[0].id == self.track_id_1
            assert tracks[1].id == self.track_id_2

        asyncio.run(run_test())

    def test_music_history_non_track_items(self):
        """Тест метода music_history когда есть элементы не типа track."""
        mock_response = {
            'history_tabs': [
                {
                    'date': '2026-01-21',
                    'items': [
                        {
                            'context': {'type': 'search'},
                            'tracks': [
                                {
                                    'type': 'track',
                                    'data': {
                                        'full_model': {
                                            'id': self.track_id_1,
                                            'title': self.track_title_1,
                                            'available': True,
                                            'available_for_premium_users': True,
                                            'duration_ms': 156210,
                                            'artists': [],
                                            'albums': [],
                                        },
                                    },
                                },
                                {
                                    'type': 'other',
                                    'data': {
                                        'full_model': {
                                            'id': '99999999',
                                            'title': 'Non Track Item',
                                        },
                                    },
                                },
                            ],
                        },
                    ],
                },
            ],
        }

        async def run_test():
            client = ClientAsync(token='test_token')  # noqa: S106
            client.base_url = 'https://api.music.yandex.net'
            client._request = AsyncMock()
            client._request.get = AsyncMock(return_value=mock_response)

            tracks = await client.music_history()

            assert isinstance(tracks, list)
            assert len(tracks) == 1
            assert tracks[0].id == self.track_id_1

        asyncio.run(run_test())
