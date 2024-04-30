export class RequestCustomEntity {

  constructor(entity) {
    this.entity = entity;
  }

  async createNewEntity(accessToken) {
    const options = {
      method: 'POST',
      headers: {
        accept: 'application/json', 
        'x-api-key': accessToken
      , 'content-type': 'application/json'
    },
      body: JSON.stringify(this.entity)
    };

    const response = await fetch('https://api.symbl.ai/v1/manage/entities', options);
    const data = await response.json();
    return data;
  }
}