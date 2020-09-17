import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouteReuseStrategy } from '@angular/router';

import { IonicModule, IonicRouteStrategy } from '@ionic/angular';
import { SplashScreen } from '@ionic-native/splash-screen/ngx';
import { StatusBar } from '@ionic-native/status-bar/ngx';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { AuthService } from './services/auth.service';
import {ViewCustomerPageModule} from './pages/view-user/modal-user.module';
import {ModalUserPage} from './pages/view-user/modal-user.page';

// TODO MOVE THE LOGIN STUFF TO THE MODEL, THEN BEFORE LOGIN THE USER NEEDS TO FILL SOME INFO ABOUT WHAT TYPE OF USER IS REGISTERING
// TODO AFTER SUBMITTING MODEL BUILD THE LINK TO TALK TO API FILLING INFO INTO DB
@NgModule({
  declarations: [AppComponent],
  entryComponents: [],
  imports: [BrowserModule, IonicModule.forRoot(), AppRoutingModule, HttpClientModule, ViewCustomerPageModule],
  providers: [
      StatusBar,
      SplashScreen,
      AuthService,
      ModalUserPage,
    {provide: RouteReuseStrategy, useClass: IonicRouteStrategy}
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
