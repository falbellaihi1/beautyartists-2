import {Component, OnInit} from '@angular/core';
import {AuthService} from '../../services/auth.service';
import { ModalController } from '@ionic/angular';


export interface UserProfile {
  name: string;
  email: string;
  image: string;

}
@Component({
  selector: 'app-user-page',
  templateUrl: 'user-page.page.html',
  styleUrls: ['user-page.scss']
})

export class UserPagePage implements OnInit{
  loginURL: string;
  logoutURL: string;
  user: UserProfile;
  constructor(public auth: AuthService) {
    this.loginURL = auth.build_login_link('tabs/user-page');
    this.logoutURL = auth.build_logout_link();

  }

  ngOnInit(): void {
    console.log('on init ');
    // const authUser = this.auth.setUser();
    // this.user.email = authUser.email;
    // this.user.name = authUser.name;
    // this.user.image = authUser.image;


  }

}
