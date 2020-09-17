import {Component, Input, OnInit} from '@angular/core';
import {ModalController} from '@ionic/angular';
import {AuthService} from '../../services/auth.service';


@Component({
    selector: 'app-view-customer',
    templateUrl: './modal-user.page.html',
    styleUrls: ['./modal-user.page.scss'],
})
export class ModalUserPage implements OnInit {
    private artist: boolean;
    loginURL: string;
    logoutURL: string;
    speciality: string;

    constructor(private modalController: ModalController,
                public auth: AuthService,
    ) {

        this.loginURL = auth.build_login_link('tabs/user-page');
        this.logoutURL = auth.build_logout_link();
    }

    async closeModal() {
        await this.modalController.dismiss();
    }

    ngOnInit() {
    }


    onCancel() {
    }


    onFocuscustomer() {
        console.log('onSelectcustomer');
        this.artist = false;
    }

    onFocusartist() {
        console.log('onSelectartist');
        // open fields?
        this.artist = true;
    }

    addArtist() {
        this.auth.saveUser(this.speciality, 'artist');
        this.closeModal();
    }

    addCustomer() {
        this.auth.saveUser('', 'customer');
        this.closeModal();
    }
    saveClicked(){

    }

}
