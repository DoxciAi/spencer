// USE THIS TO CREATE OR INTERACT WITH MANAGEMENT API
import AuthToken from './auth';
import { RequestCustomEntity } from './managementApi/entities';
import { TrackerAPI } from './managementApi/trackers';
import { config } from 'dotenv';

config();

const authToken = new AuthToken(process.env.APP_ID, process.env.APP_SECRET);
const accessToken = await authToken.getAccessToken();
// Create an instance of the TrackerAPI and RequestCustomEntity so you can Use its functions on this file
const trackerAPI = new TrackerAPI(accessToken);
const entityAPI = new RequestCustomEntity(accessToken);
