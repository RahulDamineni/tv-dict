import argparse
import asyncio
import logging
import math

from av import VideoFrame

from aiortc import (
    RTCIceCandidate,
    RTCPeerConnection,
    RTCSessionDescription,
    VideoStreamTrack,
)
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder
from aiortc.contrib.signaling import add_signaling_arguments, create_signaling


async def run(pc, player, signaling, role):
    def add_tracks():
        if player and player.audio:
            pc.addTrack(player.audio)

        if player and player.video:
            pc.addTrack(player.video)

    # @pc.on("track")
    # def on_track(track):
    #     print("Receiving %s" % track.kind)
    #     recorder.addTrack(track)

    # connect signaling
    await signaling.connect()

    if role == "offer":
        # send offer
        add_tracks()
        await pc.setLocalDescription(await pc.createOffer())
        await signaling.send(pc.localDescription)

    # consume signaling
    while True:
        obj = await signaling.receive()

        if isinstance(obj, RTCSessionDescription):
            await pc.setRemoteDescription(obj)
            await recorder.start()

            # if obj.type == "offer":
            #     # send answer
            #     add_tracks()
            #     await pc.setLocalDescription(await pc.createAnswer())
            #     await signaling.send(pc.localDescription)
        elif isinstance(obj, RTCIceCandidate):
            pc.addIceCandidate(obj)
        elif obj is None:
            print("Exiting")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video stream from the command line")
    parser.add_argument("role", choices=["offer", "answer"])
    parser.add_argument("--play-from", help="Read the media from a file and sent it."),
    parser.add_argument("--record-to", help="Write received media to a file."),
    parser.add_argument("--verbose", "-v", action="count")
    add_signaling_arguments(parser)
    args = parser.parse_args()

    # create signaling and peer connection
    signaling = create_signaling(args)
    pc = RTCPeerConnection()

    # create media source
    player = MediaPlayer(args.play_from)

    # # create media sink
    # if args.record_to:
    #     recorder = MediaRecorder(args.record_to)
    # else:
    #     recorder = MediaBlackhole()

    # run event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            run(
                pc=pc,
                player=player,
                # recorder=recorder,
                signaling=signaling,
                role=args.role,
            )
        )
    except KeyboardInterrupt:
        pass
    finally:
        # cleanup
        # loop.run_until_complete(recorder.stop())
        loop.run_until_complete(signaling.close())
        loop.run_until_complete(pc.close())
