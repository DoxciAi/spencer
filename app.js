import { MicrophoneHandler } from './utils/mic_handler.js'
import { AuthToken } from './utils/auth.js';
import { RequestCustomEntity } from './managementApi/endpoints/entities.js';
import { config } from 'dotenv';
import { v4 as uuid } from 'uuid';
import { spawn } from 'node:child_process';
import handleTranscriptions from './a_try_streaming_api.js';
import { TrackerAPI } from './managementApi/endpoints/trackers.js';


// Initialize configurations
const id = uuid();
config(); //getting access to dotenv variables
const micOptions = {
  rate: 8000,
  channels: '1',
  debug: false,
  exitOnSilence: 6,
};
const presetTargets = ['Time', 'Date', 'Location_Country', 'Person_Name', 'Brand', 'Info', 'Husband', 'Spouse', 'Other'];
const micHandler = new MicrophoneHandler(micOptions);
const authToken = new AuthToken(process.env.APP_ID, process.env.APP_SECRET);
const accessToken = await authToken.getAccessToken();
const apiUrl = `wss://api.symbl.ai/v1/streaming/${id}?access_token=${accessToken}`;
console.log('starting the WebSocket requests');
let hasSpawnBeenCalled = false;
(async () => {
  // It will run both the WebSocket and the RPA simultaneously
  handleTranscriptions(apiUrl, micHandler, presetTargets); // Will Write in A static file that must be accessed by the RPA scripts
  
  if (!hasSpawnBeenCalled) {
      await spawn('python', ["./test-sys.py"], { stdio: 'inherit' }); 
      hasSpawnBeenCalled = true;
  }
})();



