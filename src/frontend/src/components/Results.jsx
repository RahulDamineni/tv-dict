import React from 'react';
import Player from './VideoPlayer';


export default class ResultsCanvas extends React.Component {


  constructor(props) {
    super(props);

    let sampleVideo = {
      title: "Random room",
      url: "https://storage.googleapis.com/storage-tvdict/sample.mp4#t=10,12"
    }


    this.state = {
      playVideo: false,
      videoObject: sampleVideo,
      sampleVideo: sampleVideo,
      clicks: 0
    }

    this.populateMatches = this.populateMatches.bind(this)
  }

  launchPlayer(item) {
    this.setState({
      playVideo: true,
      clicks: this.state.clicks + 1,
      // videoObject: this.state.sampleVideo
      videoObject: item.videoObject
    })
    this.forceUpdate();
  }



  populateMatches(){

    return (

      <ul>
        {this.props.matches.map((item, index) => (
          <a style={{cursor: "pointer"}}
              onClick={(item) => this.launchPlayer(item)}>
            <li>
              [{item.media_path}]
              [{item.start_time} --> {item.end_time}]
              | {item.dialogue}
            </li>
          </a>
        ))}
      </ul>
    )


  }

  render() {



    let videoPlayer;
    if (this.state.playVideo) {
      videoPlayer = <Player
                        key={this.state.clicks}
                        video={this.state.videoObject}
                    />
    }

    return <div>
      {this.populateMatches()}
      {videoPlayer}
    </div>
  }
}
