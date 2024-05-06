export class RequestCustomEntity {

  constructor(accessToken) {
    this.accessToken = accessToken; //can be a object or an array of objects
  }

  async createNewEntity(entity) {
    const options = {
      method: 'POST',
      headers: {
        accept: 'application/json', 
        'x-api-key': this.accessToken
      , 'content-type': 'application/json'
    },
      body: JSON.stringify(entity)
    };

    const response = await fetch('https://api.symbl.ai/v1/manage/entities', options);
    const data = await response.json();
    return data;
  }

  async createNewEntities(entities) {
    const options = {
      method: 'POST',
      headers: {
        accept: 'application/json', 
        'x-api-key': this.accessToken
      , 'content-type': 'application/json'
    },
      body: JSON.stringify(entities)
    };

    const response = await fetch('https://api.symbl.ai/v1/manage/entities/bulk', options);
    const data = await response.json();
    return data;
  }
}