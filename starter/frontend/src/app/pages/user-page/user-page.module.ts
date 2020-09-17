import { IonicModule } from '@ionic/angular';
import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {UserPagePage} from './user-page.page';

import { ExploreContainerComponentModule } from '../explore-container/explore-container.module';

import { UserPageRoutingModule } from './user-page-routing.module';
const routes: Routes = [
  {
    path: '',
    component: UserPagePage
  }
];
@NgModule({
  imports: [
    IonicModule,
    CommonModule,
    FormsModule,
    ExploreContainerComponentModule,
    RouterModule.forChild([{ path: '', component: UserPagePage}]),
    UserPageRoutingModule,
  ],
  declarations: [UserPagePage]
})
export class UserPageModule {}
