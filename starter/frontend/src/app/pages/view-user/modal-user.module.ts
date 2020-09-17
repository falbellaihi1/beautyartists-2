import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { ViewCustomerPageRoutingModule } from './modal-user-routing.module';

import { ModalUserPage } from './modal-user.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ViewCustomerPageRoutingModule
  ],
  declarations: [ModalUserPage]
})
export class ViewCustomerPageModule {}
