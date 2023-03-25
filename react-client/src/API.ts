let api_url: string = "";

export class API {
  static setURL(url: string) {
    api_url = url;
  }

  static async CheckLogin(key: string): Promise<boolean> {
    const req = await fetch(`${api_url}/check_login`, {
      headers: { key: key },
    });

    return (await req.json()) === true;
  }
}
