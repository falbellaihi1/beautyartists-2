import {Injectable, Input} from '@angular/core';
import {JwtHelperService} from '@auth0/angular-jwt';

import {environment} from '../../environments/environment';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {ModalController} from '@ionic/angular';
import {ModalUserPage} from '../pages/view-user/modal-user.page';


const JWTS_LOCAL_KEY = 'JWTS_LOCAL_KEY';
const JWTS_ACTIVE_INDEX_KEY = 'JWTS_ACTIVE_INDEX_KEY';
const SPECIALITY = 'SPECIALITY';
const TYPE = 'TYPE';


@Injectable({
    providedIn: 'root'
})
export class AuthService {
    url = environment.auth0.url;
    audience = environment.auth0.audience;
    clientId = environment.auth0.clientId;
    callbackURL = environment.auth0.callbackURL;
    apiUrl = environment.apiServerUrl;
    token: string;
    payload: any;


    constructor(private http: HttpClient, public modalController: ModalController) {
    }

    build_login_link(callbackPath = '') {
        let link = 'https://';
        link += this.url + '.auth0.com';
        link += '/authorize?';
        link += 'audience=' + this.audience + '&';
        link += 'response_type=token&';
        link += 'client_id=' + this.clientId + '&';
        link += 'redirect_uri=' + this.callbackURL + callbackPath;

        return link;
    }

    build_logout_link(callbackPath = '') {
        console.log('logou');
        let link = 'https://';
        link += this.url + '.auth0.com';
        link += '/logout?federated&';
        link += 'returnTo=' + this.callbackURL + callbackPath + '&';
        link += 'client_id=' + this.clientId;
        return link;
    }

    async openModal() {
        /// IMPORTANT VERY BAD CIRCULAR!!!
        const modal = await this.modalController.create({
            component: ModalUserPage
        });
        return await modal.present();
    }

    saveUser(speciallity: string, type: string) {
        localStorage.setItem(TYPE, type);
        console.log(localStorage.getItem(TYPE));
        localStorage.setItem(SPECIALITY, speciallity);

    }

    createUser() {
        if (localStorage.getItem(TYPE) === 'artist') {
            // tslint:disable-next-line:max-line-length
            this.http.post(this.apiUrl + '/artist', this.setUser(), this.getHeaders())
                .subscribe((res: any) => {
                    console.log(res);
                    localStorage.removeItem(TYPE);

                });
        }
        // tslint:disable-next-line:triple-equals
        else if (localStorage.getItem(TYPE) == 'customer') {
            this.http.post(this.apiUrl + '/customer', this.setUser(), this.getHeaders())
                .subscribe((res: any) => {
                    localStorage.removeItem(TYPE);
                    console.log(res);
                });
        }
    }


    // invoked in app.component on load
    check_token_fragment() {
        // parse the fragment
        const fragment = window.location.hash.substr(1).split('&')[0].split('=');
        // check if the fragment includes the access token
        console.log(fragment);
        if (fragment[0] === 'access_token') {
            // add the access token to the jwt
            this.token = fragment[1];
            // save jwts to localstore

            this.set_jwt();
        }
    }

    getHeaders() {
        const header = {
            headers: new HttpHeaders()
                .set('Authorization', `Bearer ${this.activeJWT()}`)
        };
        return header;
    }

    set_jwt() {
        localStorage.setItem(JWTS_LOCAL_KEY, this.token);
        console.log(JWTS_LOCAL_KEY);
        if (this.token) {
            this.decodeJWT(this.token);
        }
    }

    load_jwts() {
        this.token = localStorage.getItem(JWTS_LOCAL_KEY) || null;

        if (this.token) {
            // this.decodeJWT(this.token);

        }
    }

    activeJWT() {
        return this.token;
    }


    decodeJWT(token
                  :
                  string
    ) {

        const jwtservice = new JwtHelperService();
        this.payload = jwtservice.decodeToken(token);
        this.createUser();
        return this.payload;
    }

    setUser() {
        const Userinfo = this.payload['http://localhost:8100/info'];
        const Userrole = this.payload['http://localhost:8100/roles'];
        console.log('save user ', this.payload);
        // tslint:disable-next-line:max-line-length
        const user = {
            email: Userinfo[0],
            name: Userinfo[1],
            image: Userinfo[2],
            role: Userrole,
            type: localStorage.getItem(TYPE),
            authuid: this.payload['sub'],
            speciality: localStorage.getItem(SPECIALITY)
        };
        return user;

    }

    logout() {
        this.token = '';
        this.payload = null;
        this.set_jwt();


    }

    can(permission
            :
            string
    ) {
        // tslint:disable-next-line:max-line-length
        return this.payload && this.payload.permissions && this.payload.permissions.length && this.payload.permissions.indexOf(permission) >= 0;
    }
}
