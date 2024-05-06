import { spawn } from 'node:child_process';
import WebSocket from 'ws';
import { v4 as uuid } from 'uuid';
import fs from 'fs';
import path from 'path';


export default function handleTanscriptions(apiUrl, mic, presetTargets) {
  try {
    const ws = new WebSocket(apiUrl);
    let speakerName;
    ws.on('open', () => {
      console.log('WebSocket connection established.');

      // Construct the start_request message
      const startRequest = {
        type: 'start_request',
        config: {
          confidenceThreshold: 0.7,
          detectEntities: true,
          languageCode: 'en-US',
          meetingTitle: 'My Test Meeting',
          sentiment: false,
          speechRecognition: {
            encoding: 'LINEAR16',
            sampleRateHertz: 16000
          },
        },
        //customVocabulary Array Of really different vocabulary, like company specific things
        //disconnectOnStopRequest enables resume and start options --  gotta check that out
        //disconnectOnStopRequestTimeout defines timout for closing the webSocket (default is also max 30min)
        //insightTypes can be either question or action_item -- Its an array of strings
        //noConnectionTimeout makes the webSocket be open for the time passed
        speaker: {
          name: 'Roberto',
          userId: uuid(),
        },
        //trackers is an optional object to enable trackers, if not defined, there is a default config
        //actions as sendSummary by email (The only action supported)
      };

      // Send the start_request message as JSON string
      ws.send(JSON.stringify(startRequest));
      // Check How to Handle and Send the Stop Request effectively
    });

    ws.on('message', (event) => {
      // Handle received messages
      const data = JSON.parse(event);
      if (data.type == 'message') {
        if (data && data.message.type == 'started_listening') {
          console.log("Started Listening")
          console.log('Message received:', event);
        }
        else if (data && data.message.type == 'conversation_created') {
          //This means I will finally have a conversationId
          console.log("Conversation created")
        }
        else if (data && data.message.type == 'recognition_started') {
          console.log("Recognition Started. Ready to Process Audio!!!!")
          // Here I will be handling the audio transforming to binaries(chunks) to send it to the websocket
          // It keeps waiting on this stage until we send an audio or it times out (check this further)
          mic.handleAudioStream(ws);
          // ws.send(JSON.stringify(data));
        }
        else if (data && data.message.type == 'recognition_result') {
          // console.log("This Is the Result of the Recognition")
          //console.log(data.message);
          // Handling Multiple Results of recognitions until I get a meaningful message!!
          // handleRecognitionResult(data);
        }
        else if (data && data.message.type == 'recognition_stopped') {
          console.log("Recognition Stopped. The Stop Request Was Triggered!!");
        }
        else if (data && data.message.type == 'conversation_completed') {
          console.log("Last message from API. Real-time conversation closed!!");
          return false;
        }
      }
      else if (data.type == 'message_response') {
        console.log("Final Transcript for a Message!!");
        data.messages.forEach((message) => {
          console.log(message.payload.content);
          if (message.from && message.from.name) { // check later if this actually works
          speakerName = message.from.name;
          }
        });
        //here handles the printing probably
      }
      else if (data.type === 'entity_response') {
        if (data.entities) {
          let entityMatches = {};
          if (speakerName) entityMatches.speaker = speakerName; //if there is a speaker defined then add speaker name to response object
          data.entities.forEach((entity) => {
              entity.matches.forEach((match) => {
                entityMatches[entity.subType] = match.detectedValue;
              });
          });
          //Sending complete entity object to RPA Manager
          //Maybe We will have to Set a Queue for this, so it will run only on completion of previous async task
          if (Object.keys(entityMatches).length > 0) {
            // console.log('Entity Detected:', entityMatches);
            // const pythonProcess = spawn('python', ["./test-sys.py", JSON.stringify(entityMatches)], { stdio: 'inherit' });
          }
        }
      }
      else if (data.type === 'tracker_response') {
        let i = 0;
        data.trackers.forEach((tracker) => {
          let trackerMatch = {};
          trackerMatch.name = tracker.name;
          tracker.matches.forEach((match) => {
            trackerMatch.type = match.type;
            match.messageRefs.forEach((messageRef) => {
              trackerMatch.messageRefs = messageRef.text;
            });
          });
          const filePath = path.join('./', 'data', `tracker_${trackerMatch.name}_${i++}.json`);
          fs.writeFile(filePath, JSON.stringify(trackerMatch, null, 2), (err) => {
              if (err) throw err;
              console.log(`Tracker has been saved!`);
          });
        });
      }
    });

    ws.on('error', (error) => {
      console.error('WebSocket error:', error);
    });

    } catch (error) {
      console.error('WebSocket error:', error);
    }
}