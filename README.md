# process_audio

Simple python tool that can:
- reverse an audio file
- concatenate audio files
- split an audio file by timestamps

## dependenices

- pydub
- ffmpeg (to process different audio formats)

## examples

```
./process_audio reverse original.mp3 reversed.mp3

./process_audio concatenate head.mp3 body.mp3 tail.mp3 result.mp3

./process_audio split file.mp3 "[0:10 0:15]" "[1:12 1:34]" output.mp3
```

Or you can build a docker image with provided Dockerfile, but to communicate your files with docker you should set up a docker volume

```
docker build -t process_audio .
docker run -v /home/username/Music:/code/Music process_audio:latest reverse Music/file.wav Music/rev.wav
```
