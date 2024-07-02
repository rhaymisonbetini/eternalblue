from setuptools import setup

setup(
    name='eternalblue',
    version='0.1.0',
    description='Um pacote de diarização',
    url='https://github.com/seu_usuario/eternalblue',
    author='Rhaymison Betini',
    author_email='rhaymisoncristian@gmail.com',
    license='Apache 2.0',
    packages=['eternalblue'],
    install_requires=[
        'transformers~=4.38.2',
        'pyannote.audio',
        'torch~=2.1.2',
        'torchaudio~=2.1.2',
        'torchvision',
        'pydub~=0.25.1',
        'accelerate',
        'noisereduce~=3.0.2',
        'librosa~=0.10.1',
        'python-dotenv',
        'soundfile~=0.12.1',
        'bitsandbytes',
        'insanely-fast-whisper',
        'optimum',
        'openai'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.10',
)
