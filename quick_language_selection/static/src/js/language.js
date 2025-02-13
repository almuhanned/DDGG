/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
const { Component} = owl;
console.log("owl",owl);
// const { useState } = hooks;


export class SwitchLanguageMenu extends Component {
    async setup() {
        var session = require('web.session');
        var self = this;
        
        var rpc = require('web.rpc');
        
        var languages =await  rpc.query({
            model: 'res.lang',
            method: 'search_read',
            args: [[],['name', 'code']],
        }).then(function (res) {
            return res;
            // console.log("lang",res)
            // var x = 0;
            // _.each(res, function (lang) {
                // language_list[x] = lang;
            //     x += 1;
            // });
        });    
        console.log(languages,"languages");
        self.languageService = languages;
        self.currentLanguage = session.user_context.lang;
        }

    async logIntoLanguage(language) {
        console.log("language js",language.length);
        var self = this;
        var session = require('web.session');
        var rpc = require('web.rpc');
        console.log(session.uid,"user id")
        let is_changed=await rpc.query({
            model: 'res.users',
            method: 'write',
            args: [session.uid, {'lang':language['code']}],
        }).then(function (result) {
            return result;
            // 
        });
        if(is_changed){
            
            window.location.reload();
            //  caches.delete().then(()=>{
            //     window.loc
            //  })    
            

            
        }
        console.log(is_changed,"is changed");
        };    
}
SwitchLanguageMenu.template = "quick_language_selection.SwitchLanguageMenu";
SwitchLanguageMenu.toggleDelay = 1000;
SwitchLanguageMenu.components = { Dropdown, DropdownItem };
const systrayItem = {
    Component: SwitchLanguageMenu,
    isDisplayed(env) {
        return Object.keys([]);
    },
   
};

registry.category("systray").add("SwitchLanguageMenu", systrayItem, { sequence: 2 })
