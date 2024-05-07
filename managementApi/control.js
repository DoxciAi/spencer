// USE THIS TO CREATE OR INTERACT WITH MANAGEMENT API
import { AuthToken } from '.././utils/auth.js';
import { RequestCustomEntity } from './endpoints/entities.js';
import { TrackerAPI } from './endpoints/trackers.js';
import { config } from 'dotenv';

config({ path: '../.env' });
const authToken = new AuthToken(process.env.APP_ID, process.env.APP_SECRET);
const accessToken = await authToken.getAccessToken();
const trackerAPI = new TrackerAPI(accessToken);
const entityAPI = new RequestCustomEntity(accessToken);

const tracker = {
  "name": "Managing a Budget",
  "description": "Focuses on strategies and tools for effectively planning, tracking, and controlling personal or organizational finances within a predefined spending limit.",
  "categories": ["Financial Priorities"],
  "languages": ["en-US"],
  "vocabulary": [
    "budgeting",
    "income",
    "expenses",
    "savings",
    "spending",
    "fixed expenses",
    "variable expenses",
    "discretionary expenses",
    "budget planner",
    "budget spreadsheet",
    "budgeting app",
    "budget categories",
    "budget allocation",
    "budget surplus",
    "budget deficit",
    "emergency fund",
    "financial goals",
    "budget review",
    "budget adjustments",
    "cash flow",
    "financial tracking",
    "expense tracking",
    "financial discipline"
  ]
}


const apiResponse = await trackerAPI.createTracker(tracker)
console.log(apiResponse);