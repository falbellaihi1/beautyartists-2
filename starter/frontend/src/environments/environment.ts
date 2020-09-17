// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
    production: false,
    apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
    auth0: {
        url: 'falbellaihi1.us', // the auth0 domain prefix
        audience: 'beautyartists', // the audience set for the auth0 app
        clientId: 'yIxTUTt29qis1zN53vsx6efjY7Uk2p80', // the client id generated for the auth0 app
        callbackURL: 'http://localhost:8100/', // the base url of the running ionic application.
    }
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.
