export class TrackerAPI {
  constructor(accesstoken) {
    this.accesstoken = accesstoken;
  }

  async createTracker(tracker) {
    const options = {
      method: 'POST',
      headers: {
        accept: 'application/json',
        'x-api-key': this.accesstoken,
        'content-type': 'application/json'
      },
      body: JSON.stringify(tracker)
    };

    const response = await fetch('https://api.symbl.ai/v1/manage/trackers', options);
    const data = await response.json();
    return data;
  }
}