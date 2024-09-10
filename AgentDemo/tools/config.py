API_KEY = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiLmt7HlnLPlvpfnkIbnp5HmioDmnInpmZDlhazlj7giLCJVc2VyTmFtZSI6Iuaut-m-mSIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxNzkzMjYxMDE0NTU3Mzk3NzIxIiwiUGhvbmUiOiIxODEyNDY1NDU5NyIsIkdyb3VwSUQiOiIxNzkzMjYxMDE0NTQ5MDA5MTEzIiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoiIiwiQ3JlYXRlVGltZSI6IjIwMjQtMDctMTIgMTI6MzY6MzciLCJpc3MiOiJtaW5pbWF4In0.nysgoLnspkts3ZImmROY3dO3CE23E0-D_miH4bj8kq574omVVcXqO3Wd4PpH-OD3OOoCp7dP1Ah47q3sj06DC82ubOdruBJ291eWoyR3lIjR-F8tQG5xu5nfkAeAilh_8VOshlCiwNsTixwLWo8fymvWgM-ySd5x2MHhhAXVHVjYA7R8ORKDFW8mLET7KnKC662JzTAb0ObPcpAVDiPUfReyjjjAQAPBa3juY0SuPKSPsUtnH-7I050Hlf6s3RpkI2xLZiIJurmSej1M25nJA3o6yvisdVCvRoM-pKFpukFH40nRyOO_S3fBoVSG81IWS9nuxeNJj7OnC0v4cH9jmQ"

URL = f"https://api.minimax.chat/v1/t2a_pro"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}
data = {
    "voice_id": None,
    # 如同时传入voice_id和timber_weights时，则会自动忽略voice_id，以timber_weights传递的参数为准
    "text": None,
    # 如需要控制停顿时长，则增加输入<#X#>，X取值0.01-99.99，单位为秒，如：你<#5#>好（你与好中间停顿5秒）需要注意的是文本间隔时间需设置在两个可以语音发音的文本之间，且不能设置多个连续的时间间隔。
    "model": "speech-01",
    "speed": 1.0,
    "vol": 1.0,
    "pitch": 0,
    "audio_sample_rate": 24000,
    "bitrate": 128000,
    "timber_weights": [
        {
            "voice_id": "female-shaonv",
            "weight": 1
        },
        {
            "voice_id": "presenter_female",
            "weight": 5
        },
        {
            "voice_id": "female-yujie",
            "weight": 1
        },
        {
            "voice_id": "female-tianmei",
            "weight": 1
        }
    ]
}
