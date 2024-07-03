this._hd=this._hd||{};(function(_){var window=this;
try{
_.Eu=_.Un("BUYwVb");_.Hwb=_.Un("LsLGHf");
}catch(e){_._DumpException(e)}
try{
_.Nwb=_.Bd("DPreE",[_.bq,_.dq]);
}catch(e){_._DumpException(e)}
try{
_.Owb=function(a){this.Ea=_.n(a)};_.A(_.Owb,_.q);_.Pwb=function(a,b){return _.fj(a,1,b)};_.Qwb=function(a,b){return _.fj(a,2,b)};_.Rwb=function(a,b){return _.Dg(a,5,b)};_.Swb=function(a,b){return _.Dg(a,6,b)};_.Twb=function(a,b){return _.Dg(a,7,b)};_.Uwb=function(a,b){return _.Dg(a,8,b)};_.Vwb=function(a,b){return _.Dg(a,9,b)};_.Wwb=function(a,b){return _.Dg(a,10,b)};_.Xwb=function(a,b){return _.Dg(a,11,b)};_.Ywb=function(a,b){return _.Dg(a,12,b)};_.Zwb=function(a,b){return _.Dg(a,13,b)};
_.Owb.prototype.kb="mVjAjf";
}catch(e){_._DumpException(e)}
try{
_.Gu=function(a,b,c,d,e,f,g,h,k){var m=_.$wb(c),p=_.sm.getBounds(a),r=_.sm.o_(a);r&&_.mBa(p,_.kBa(r));_.sm.KPd(p,_.Qe(a),_.Qe(c));a=_.axb(a,b);b=p.left;a&4?b+=p.width:a&2&&(b+=p.width/2);p=new _.bl(b,p.top+(a&1?p.height:0));p=_.yya(p,m);e&&(p.x+=(a&4?-1:1)*e.x,p.y+=(a&1?-1:1)*e.y);if(g)if(k)var u=k;else if(u=_.sm.o_(c))u.top-=m.y,u.right-=m.x,u.bottom-=m.y,u.left-=m.x;return _.bxb(p,c,d,f,u,g,h)};
_.$wb=function(a){if(a=a.offsetParent){var b=a.tagName=="HTML"||a.tagName=="BODY";if(!b||_.sm.Zha(a)!="static"){var c=_.sm.eI(a);b||(c=_.yya(c,new _.bl(_.sm.vj.jz(a),a.scrollTop)))}}return c||new _.bl};_.bxb=function(a,b,c,d,e,f,g){a=a.clone();var h=_.axb(b,c);c=_.sm.getSize(b);g=g?g.clone():c.clone();a=_.cxb(a,g,h,d,e,f);if(a.status&496)return a.status;_.sm.setPosition(b,a.rect.wy());g=a.rect.getSize();_.zya(c,g)||_.sm.lHd(b,g);return a.status};
_.cxb=function(a,b,c,d,e,f){a=a.clone();b=b.clone();var g=0;if(d||c!=0)c&4?a.x-=b.width+(d?d.right:0):c&2?a.x-=b.width/2:d&&(a.x+=d.left),c&1?a.y-=b.height+(d?d.bottom:0):d&&(a.y+=d.top);if(f){if(e){g=a;c=b;d=0;(f&65)==65&&(g.x<e.left||g.x>=e.right)&&(f&=-2);(f&132)==132&&(g.y<e.top||g.y>=e.bottom)&&(f&=-5);g.x<e.left&&f&1&&(g.x=e.left,d|=1);if(f&16){var h=g.x;g.x<e.left&&(g.x=e.left,d|=4);g.x+c.width>e.right&&(c.width=Math.min(e.right-g.x,h+c.width-e.left),c.width=Math.max(c.width,0),d|=4)}g.x+c.width>
e.right&&f&1&&(g.x=Math.max(e.right-c.width,e.left),d|=1);f&2&&(d|=(g.x<e.left?16:0)|(g.x+c.width>e.right?32:0));g.y<e.top&&f&4&&(g.y=e.top,d|=2);f&32&&(h=g.y,g.y<e.top&&(g.y=e.top,d|=8),g.y+c.height>e.bottom&&(c.height=Math.min(e.bottom-g.y,h+c.height-e.top),c.height=Math.max(c.height,0),d|=8));g.y+c.height>e.bottom&&f&4&&(g.y=Math.max(e.bottom-c.height,e.top),d|=2);f&8&&(d|=(g.y<e.top?64:0)|(g.y+c.height>e.bottom?128:0));e=d}else e=256;g=e}e=new _.rm(0,0,0,0);e.left=a.x;e.top=a.y;e.width=b.width;
e.height=b.height;return{rect:e,status:g}};_.axb=function(a,b){return(b&8&&_.sm.Xi(a)?b^4:b)&-9};
}catch(e){_._DumpException(e)}
try{
_.y("DPreE");
var Hu=function(a){_.mf.call(this,a.Oa);var b=this;this.offsetY=this.offsetX=0;this.Ka=this.Ca=!1;this.data=a.jsdata.Z5c;this.ka=a.service.dismiss;this.ij=a.service.ij;this.root=this.getRoot().el();this.popup=this.Ma("V68bde").Ab();_.eo(this,this.popup);this.Fa=function(){b.reposition()};_.Xd(window,"resize",this.Fa);this.Na=this.Bp().hasAttribute("role");this.Ka=_.C(this.data,13);this.wa()};_.A(Hu,_.mf);Hu.Ia=function(){return{jsdata:{Z5c:_.Owb},service:{dismiss:_.yu,ij:_.Cu}}};_.l=Hu.prototype;
_.l.kc=function(){this.oa()&&this.isVisible()?this.ka.dismiss(this.popup):this.ka.unlisten(this.popup);_.Pk(window,"resize",this.Fa);_.rf(this.root,this.popup)||this.root.appendChild(this.popup);_.mf.prototype.kc.call(this)};
_.l.onDismiss=function(a,b,c){if((c=c===void 0?null:c)&&_.Ca(c)&&c.nodeType>0&&_.rf(this.Bp(),c)||a.some(function(d){return _.rf(d,c)}))return!1;if(_.C(this.data,12))return this.trigger(_.Mwb,{type:b,Lw:c}),!0;this.setVisible(!1);_.lf(document,_.Mwb);b===2&&(a=this.Bp(),a.hasAttribute("tabindex")||(a=a.firstElementChild),a.focus());return!0};
_.l.Mm=function(a){var b=this,c=a.event;if(!c)return!1;c=c.which||c.keyCode;c!==40&&c!==38||!this.getPopup().querySelector("g-menu")||(this.ij.disable(),this.gTa(a),(0,_.qn)(function(){b.ij.enable()},0));return!1};_.l.gTa=function(a){var b=a.event||void 0,c=a.tb.el();c.focus();_.Xc(c)&&_.tu(c);a=a.data&&a.data.nonDismissingElements||[];this.setVisible(!this.isVisible(),b,this.Bp().firstElementChild,a);b&&(b=_.re(b))&&b.preventDefault()};
_.l.reposition=function(){if(this.isVisible()){var a=this.getPopup(),b=this.Bp(),c=new _.bl(this.offsetX,this.offsetY),d=_.mi(this.data,1),e=_.mi(this.data,2);d=dxb(d);e=dxb(e);if(b.offsetParent===null&&b.style.position!=="fixed")this.dismiss();else{if(_.C(this.data,7)){var f=_.sm.getSize(b).width;if(_.C(this.data,9)){_.sm.zd(a,"");var g=_.sm.getSize(a).width;g>f&&(f=g)}_.sm.zd(a,f)}f=(_.C(this.data,5)?1:0)|(_.C(this.data,6)?4:0);if((g=window.visualViewport)&&g.scale!==1){var h=_.$wb(this.getPopup());
g=new _.qm(g.pageTop-h.y,g.pageLeft+g.width-h.x,g.pageTop+g.height-h.y,g.pageLeft-h.x)}else g=void 0;_.Gu(b,d,a,e,c,void 0,f,void 0,g)}}};_.l.isVisible=function(){return _.sm.Qh(this.getPopup())};_.l.dismiss=function(){this.isVisible()&&this.ka.dismiss(this.popup)};
_.l.setVisible=function(a,b,c,d){var e=this;d=d===void 0?[]:d;var f=this.getPopup(),g=a!==this.isVisible(),h=a?_.Jwb:_.Kwb;_.sm.Rb(f,a);a&&_.rf(this.root,f)?_.C(this.data,8)||_.Du().appendChild(f):a||_.rf(this.root,f)||this.root.appendChild(f);a&&(this.trigger(_.Iwb,{popup:this}),this.reposition());g&&(this.Na&&this.Bp().setAttribute("aria-expanded",a?"true":"false"),a?(this.Ka&&_.qu([new _.ln(this.popup,"show")]),this.Ca||(this.Ca=!0,_.lf(f,_.Eu),_.lf(f,h)),this.oa()?this.ka.listen(this.popup,function(k,
m){return e.onDismiss(d,k,m)},[].concat(_.nd(exb),[4]),!1,!0,!1,function(){e.setVisible(a,b,c,d)},this.getData("bbena").string()||this.root.getAttribute("jsname")):(f=_.C(this.data,10)?fxb:_.C(this.data,11)?gxb:exb,this.ka.listen(this.popup,function(k,m){return e.onDismiss(d,k,m)},f,!1,!0))):this.ka.unlisten(this.popup),this.trigger(h,{wc:c||null,FNa:(b?b.which||b.keyCode:null)===38?!0:!1,Ux:b}))};_.l.Bp=function(){return this.Ma("oYxtQd").el()};_.l.getPopup=function(){return this.popup};
_.l.QIa=function(a,b){this.offsetX=a;this.offsetY=b};var dxb=function(a){var b=8;switch(a){case 2:b=2;break;case 1:b=8;break;case 3:b=12;break;case 5:b=3;break;case 4:b=9;break;case 6:b=13}return b};Hu.prototype.oa=function(){var a=this.getData("bbena"),b=a.string("")||this.root.getAttribute("jsname");return!(!a.Lb()||!b)};Hu.prototype.wa=function(){var a=this;this.oa()&&this.ka.Kb(function(){a.setVisible(!0)},this.getData("bbena").string()||this.root.getAttribute("jsname"))};
_.G(Hu.prototype,"NjCoec",function(){return this.wa});_.G(Hu.prototype,"OOY56c",function(){return this.oa});_.G(Hu.prototype,"pcAkKe",function(){return this.getPopup});_.G(Hu.prototype,"vBAC5",function(){return this.Bp});_.G(Hu.prototype,"IYtByb",function(){return this.dismiss});_.G(Hu.prototype,"eO2Zfd",function(){return this.isVisible});_.G(Hu.prototype,"xKqF2c",function(){return this.reposition});_.G(Hu.prototype,"WFrRFb",function(){return this.gTa});_.G(Hu.prototype,"uYT2Vb",function(){return this.Mm});
_.G(Hu.prototype,"k4Iseb",function(){return this.kc});_.ir(_.Nwb,Hu);var exb=[1,2,3],fxb=[1,3],gxb=[1,2];
_.z();
}catch(e){_._DumpException(e)}
try{
_.LXc=_.Bd("P10Owf",[_.gq]);
}catch(e){_._DumpException(e)}
try{
_.y("P10Owf");
var kC=function(a){_.mf.call(this,a.Oa);this.ka=this.getData("cmep").Lb();this.Pb=a.service.Pb;this.data=a.Zd.Bda};_.A(kC,_.mf);kC.Ia=function(){return{service:{Pb:_.Ft},Zd:{Bda:_.NB}}};kC.prototype.Ca=function(){this.Pb.ka().oa(this.getRoot().el(),1).log(!0)};kC.prototype.wa=function(a){a=a.data?_.$b(_.NB,a.data):new _.NB;MXc(this,a)};kC.prototype.oa=function(a){MXc(this,a.data)};
var MXc=function(a,b){var c;(b==null?0:_.QB(b))&&((c=a.data)==null?0:_.QB(c))&&(b==null?void 0:_.QB(b))!==_.QB(a.data)||a.Pb.ka().oa(a.getRoot().el(),2).log(!0)};kC.prototype.Ka=function(a){this.Pb.ka().ka(a.tb.el()).log(!0);_.lf(document,_.mjc)};kC.prototype.Fa=function(a){this.Pb.ka().ka(a.tb.el()).log(!0);if(this.ka){var b;_.lf(document,_.ljc,(b=this.data)==null?void 0:b.Qc())}else _.lf(document,_.kjc,this.data)};_.G(kC.prototype,"kEOk4d",function(){return this.Fa});_.G(kC.prototype,"fT3Ybb",function(){return this.Ka});
_.G(kC.prototype,"hRwSgb",function(){return this.oa});_.G(kC.prototype,"s5CUif",function(){return this.wa});_.G(kC.prototype,"MlP2je",function(){return this.Ca});_.ir(_.LXc,kC);
_.z();
}catch(e){_._DumpException(e)}
try{
_.y("WlNQGd");
var Z3b=function(a,b,c){this.trigger=a;this.QGd=b;this.qH=c},Ax=function(a){_.mf.call(this,a.Oa);this.Fa=null;this.Ka=[];this.oa=null;this.prefix="";this.Lta=[].concat(_.nd(a.controllers.Lta),_.nd(a.controllers.YGd),_.nd(a.controllers.MZc));this.menu=this.getRoot().el();this.Qa=_.qBa(this.menu)==="listbox";this.Ua=new _.Iq(this.qb,1E3,this);_.zg(this,this.Ua);$3b(this)};_.A(Ax,_.mf);Ax.Ia=function(){return{controllers:{Lta:"NNJLud",YGd:"hgDUwe",MZc:"tqp7ud"}}};Ax.prototype.Ya=function(){return this.oa};
Ax.prototype.wa=function(){var a=this,b=[].concat(_.nd(this.yb("NNJLud").toArray())).filter(function(d){return!a.ka(d).f8a()}),c=_.bo(this,"tqp7ud").el();c&&b.push(c);return b};Ax.prototype.Za=function(){return this.Lta};Ax.prototype.qb=function(){this.prefix=""};
var $3b=function(a){var b=a.wa();_.Fa(b,function(c){var d=a.ka(c);if(d.isSelected()&&d.isEnabled())switch(d.getType()){case 2:a4b(a);d.Bw(!0);a.Fa=c;break;case 3:d.Bw(!0);a.Ka.push(c);break;default:d.Bw(!1)}else d.Bw(!1)},a);b=b[0];a.ka(b).Gbb()&&b.setAttribute("tabindex","0")};
Ax.prototype.clearSelection=function(){for(var a=_.Na(this.wa()),b=a.next();!b.done;b=a.next()){b=this.ka(b.value);if(b.isSelected()&&b.isEnabled())switch(b.getType()){case 2:a4b(this);break;case 3:this.Ka.pop();break;case 1:case 7:case 6:case 4:case 5:case 10:break;default:b.getType()}b.Bw(!1)}b4b(this,null)};var a4b=function(a){a.Fa&&(a.ka(a.Fa).Bw(!1),a.Fa=null)};Ax.prototype.ka=function(a){return this.Lta.find(function(b){return b.getRoot().el()===a})};
var c4b=function(a,b){return!!a.wa().find(function(c){return c===b})};Ax.prototype.Ca=function(a,b){b=b===void 0?!1:b;c4b(this,a)&&d4b(this,a,b)};
var d4b=function(a,b,c){var d=a.ka(b);if(d.isEnabled()){b4b(a,b);switch(d.getType()){case 2:var e=a.Fa!==b;e&&(a4b(a),a.Fa=b,d.Bw(!0));e4b(a,d,e,c);break;case 3:e=!d.isSelected();d.Bw(e);e?a.Ka.push(b):_.va(a.Ka,b);e4b(a,d,!0,c);break;case 5:a=a.getRoot().el();_.ze(a,_.V3b);break;default:e4b(a,d,!1,c)}d.isSelected()}},e4b=function(a,b,c,d){a=a.getRoot().el();_.ze(a,_.U3b,new Z3b(b,c,d))};_.l=Ax.prototype;_.l.Kt=function(){return this.Fa};_.l.R9c=function(){return this.Ka};_.l.A8c=function(){return this.oa};
_.l.YBa=function(){var a=this.Kt();return a?this.ka(a).getContent():""};_.l.t_b=function(){var a=this.wa()[0];return a?this.L2(a):null};_.l.d0b=function(a){a=a===void 0?!1:a;var b=this.Kt();b&&this.Qa?a=b:a?a=(a=_.na(this.wa()))?this.L2(a):null:a=this.t_b();return a};
_.l.L2=function(a){var b=this.ka(a);if(b.getType()!==6&&b.getType()!==10)return a;b=(new _.jg([a])).find("*").toArray();return(a=[a].concat(b).find(function(c){return _.me(c)&&_.sm.Qh(c)&&(c.getAttribute("role")==="menuitem"&&c.hasAttribute("tabindex")||_.Ll(c))}))?a:null};_.l.Tma=function(a){a&&!c4b(this,a)||b4b(this,a)};
var b4b=function(a,b,c){c=c===void 0?!1:c;if(b){var d=a.ka(b);if(!d.isEnabled()&&c)return;d.RJb(!0);d.Gbb()&&b.setAttribute("tabindex","0")}else a.menu.setAttribute("tabindex","0"),a.menu.focus();a.oa!==b&&a.oa&&(c=a.ka(a.oa),c.Gbb()&&a.oa.setAttribute("tabindex","-1"),c.RJb(!1));a.oa=b},f4b=function(a){a=a.targetElement;for(var b,c;a.el()!=null&&((b=a.el())==null?void 0:b.tagName)!=="G-MENU-ITEM"&&((c=a.el())==null?void 0:c.tagName)!=="G-MENU";)a=a.parent();var d;return((d=a.el())==null?void 0:d.tagName)===
"G-MENU-ITEM"?a.el():null};_.l=Ax.prototype;_.l.pfd=function(a){var b=f4b(a);if(b){var c=a.event;(c=c?c.which||c.keyCode:null)&&c===32?this.Mm(a):d4b(this,b,!0)}};_.l.Asc=function(){this.oa===null&&b4b(this,this.wa()[0])};_.l.Bsc=function(){var a=this.getRoot().el();_.ze(a,_.W3b)};_.l.Csc=function(){var a=this.getRoot().el();_.ze(a,_.X3b);b4b(this,null)};_.l.Bfd=function(a){(a=f4b(a))&&b4b(this,a,!0)};
_.l.Mm=function(a){var b=a.event;if(!b||b.ctrlKey||b.metaKey||b.shiftKey||b.altKey)return!1;var c=b.which||b.keyCode,d=!1;if(c===27)return!0;if(c===40||c===38){var e=this.oa,f=this.wa();e=c===38?e===f[0]:e===f.pop();if(!this.Qa||!e){c=40===c;e=g4b(this,c);var g;c=(g=c?e.shift():e.pop())!=null?g:null;b4b(this,c);this.Na(this.oa)}}else if(c===13||c===32&&!this.prefix)this.oa&&(d=this.ka(this.oa).getType()===6||this.ka(this.oa).getType()===10,d4b(this,this.oa,!0));else if(_.vBa(c))this.Ua.start(),g=
String.fromCharCode(c),this.prefix===g?g=h4b(this,!0):(this.prefix+=g,g=h4b(this,!1)),g&&(b4b(this,g),this.Na(this.oa));else return!1;a.tb.el().contains(b.target)&&(_.ar(b),d||_.se(b));return!1};
var h4b=function(a,b){return(b?g4b(a,!0):a.wa()).find(function(c){return a.ka(c).isEnabled()?(c=a.ka(c).getContent(),_.rta(c,a.prefix)):!1})},g4b=function(a,b){var c=a.oa,d=a.wa().filter(function(e){return _.sm.Qh(e)});c===null&&(a.menu.getAttribute("tabindex")==="0"||d.length>0&&d[0].getAttribute("tabindex")==="0")&&(c=b?_.na(d):d[0]);c&&(a=d.findIndex(function(e){return c===e}),d=_.mcb(d,b?-a-1:-a),a=d.findIndex(function(e){return c===e}));return d};
Ax.prototype.Na=function(a){a&&(this.Ra(a),(a=this.L2(a))&&a.focus())};
Ax.prototype.Ra=function(a,b){if(a){var c=_.sm.getSize(this.menu);if(c.height<this.menu.scrollHeight){var d=this.menu.getBoundingClientRect().top,e=_.sm.getSize(a);d=a.getBoundingClientRect().top-d;var f=e.height/2;d<f?this.menu.scrollTop+=d-f:d+e.height>c.height-f&&(this.menu.scrollTop+=d+e.height-c.height+f);b&&(this.menu.scrollTop+=a.getBoundingClientRect().top-this.menu.getBoundingClientRect().top-Math.floor((c.height-e.height)/2))}}};_.G(Ax.prototype,"uYT2Vb",function(){return this.Mm});
_.G(Ax.prototype,"IgJl9c",function(){return this.Bfd});_.G(Ax.prototype,"Tx5Rb",function(){return this.Csc});_.G(Ax.prototype,"WOQqYb",function(){return this.Bsc});_.G(Ax.prototype,"h06R8",function(){return this.Asc});_.G(Ax.prototype,"PSl28c",function(){return this.pfd});_.G(Ax.prototype,"xpRsNe",function(){return this.t_b});_.G(Ax.prototype,"OG2qqc",function(){return this.YBa});_.G(Ax.prototype,"kvm28d",function(){return this.A8c});_.G(Ax.prototype,"mFs2Sc",function(){return this.R9c});
_.G(Ax.prototype,"Urwwkf",function(){return this.Kt});_.G(Ax.prototype,"J2hPTe",function(){return this.clearSelection});_.G(Ax.prototype,"gSmKPc",function(){return this.Za});_.G(Ax.prototype,"lSpRlb",function(){return this.wa});_.G(Ax.prototype,"mJ60jb",function(){return this.Ya});_.ir(_.Y3b,Ax);
_.z();
}catch(e){_._DumpException(e)}
try{
_.y("kQvlef");
var SRb,URb,VRb,WRb;_.TRb=function(a,b){return _.zc(SRb.exec(_.Bc(a).toString())[0]+"#"+b)};SRb=/[^#]*/;URb=_.Kg(["/",""]);VRb=_.ba.gapi;_.Pw=function(a){_.En.call(this,a.Oa);this.iframe=null;this.window=a.service.window;a=this.window.get().location;this.wa=new RegExp("^("+a.protocol+"//"+a.host+")?/(url|aclk)\\?.*&rct=j(&|$)")};_.A(_.Pw,_.En);_.Pw.Va=_.En.Va;_.Pw.Ia=function(){return{service:{window:_.Fn}}};
_.Pw.prototype.oa=function(a,b){b=b===void 0?!1:b;var c=!1;try{this.wa.test(a)&&(_.ud("google.r",1),WRb(this).src=a,c=!0)}finally{c||(c=this.window.get().location,b?_.Rha(c,_.mc(a)):c.href=a)}};
_.Pw.prototype.ka=function(a,b){b=b===void 0?!1:b;var c=!1;try{var d=a instanceof _.Kc?_.Bc(a).toString():a instanceof _.jc?_.lc(a):a;if(this.wa.test(d)){_.ud("google.r",1);var e,f=((e=_.Vka(d))!=null?e:"").substring(1),g=_.Ac(URb,f),h,k=new Map((new URLSearchParams((h=_.Wd(6,d))!=null?h:"")).entries()),m=_.Cc(g,k),p=_.cm(d);var r=p?_.TRb(m,p):m;_.Ic(WRb(this),r);c=!0}}finally{c||(a=a.toString(),c=b,c=c===void 0?!1:c,b=this.window.get().location,_.XRb&&!_.YRb&&VRb.iframes.getContext().getParentIframe()!=
null?(c=VRb.iframes.getContext().getParentIframe(),a.match("^/[^/]+")&&(a=b.protocol+"//"+b.host+a),c.send("navigate",{href:a},void 0,VRb.iframes.CROSS_ORIGIN_IFRAMES_FILTER)):c?_.Rha(b,a):_.Mc(b,a))}};WRb=function(a){a.iframe||(a.iframe=_.xl("IFRAME"),a.iframe.style.display="none",_.yl(a.iframe));return a.iframe};_.XRb=!1;_.YRb=!1;_.Gn(_.eq,_.Pw);
_.z();
}catch(e){_._DumpException(e)}
try{
_.l5b=_.Un("w3Ukrf");_.m5b=_.Un("gXfOqb");_.n5b=_.Un("n1Iq3");_.o5b=_.Un("x6BCfb");_.p5b=_.Un("BVfjhf");
}catch(e){_._DumpException(e)}
try{
_.r5b=_.Bd("fXO0xe",[_.Up,_.eq]);
}catch(e){_._DumpException(e)}
try{
_.y("fXO0xe");
var s5b=function(a){_.mf.call(this,a.Oa);this.wa=!1;this.ka=null;this.rootElement=this.getRoot().el();this.Ca=_.Nl(this.rootElement,"g-menu-item");this.Ka=this.getData("hbc").string("");this.Na=this.getData("htc").string("");this.Qa=this.getData("bsdm").bool(!1);this.Ra=this.getData("tsdm").bool(!1);this.Fa=this.getData("btf").bool(!1);this.oa=this.Qa||this.Fa||this.Ra;this.Ua=this.getData("spt").bool();this.od=a.service.location;this.Lc=a.service.navigation};_.A(s5b,_.mf);
s5b.Ia=function(){return{service:{location:_.Au,navigation:_.Pw}}};_.l=s5b.prototype;_.l.Lsc=function(){var a=a===void 0?null:a;var b=document.getElementById("YUIDDb");this.Ua&&b?(_.tu(this.rootElement,{Mo:1}),b=new _.Jm(b.getAttribute("data-spl")),a!=null&&_.Sm(b,"cs",a),this.Lc.oa(b.toString())):(_.tu(this.rootElement),a=_.Um(new _.Jm(this.od.Wi()),"hl")||"",a=_.Qm(_.Sm(_.Sm(new _.Jm("/preferences"),"prev",this.od.Wi()),"hl",a),"appearance"),this.Lc.oa(a.toString()))};
_.l.Msc=function(){var a=this;this.oa&&(_.sm.setStyle(this.Ca,{background:this.Ka,color:this.Na}),this.trigger(_.Lwb),this.wa=!0,_.Xd(document,"click",function(){a.Q2b()},{once:!0,passive:!0}))};_.l.Q2b=function(){var a=this;this.oa&&(this.ka=_.Xd(document,"click",function(){a.b3b()},{once:!0,passive:!0}))};_.l.b3b=function(){this.oa&&(_.sm.setStyle(this.Ca,{background:"",color:""}),this.ka&&(_.Qk(this.ka),this.ka=null))};_.l.Khd=function(){this.wa&&(this.wa=!1,this.trigger(_.p5b))};
_.G(s5b.prototype,"aelxJb",function(){return this.Khd});_.G(s5b.prototype,"MB7MSb",function(){return this.b3b});_.G(s5b.prototype,"fbAr9c",function(){return this.Q2b});_.G(s5b.prototype,"ggFCce",function(){return this.Msc});_.G(s5b.prototype,"ok5gFc",function(){return this.Lsc});_.ir(_.r5b,s5b);
_.z();
}catch(e){_._DumpException(e)}
try{
_.SRc=_.Un("dl3bm");_.TRc=_.Un("EbPWYd");
}catch(e){_._DumpException(e)}
try{
_.VRc=_.Bd("gSZvdb",[]);
}catch(e){_._DumpException(e)}
try{
_.y("gSZvdb");
var WRc=function(a){_.mf.call(this,a.Oa);this.wa=this.getData("msf").Lb();this.ka=this.getData("cmep").Lb();this.data=a.jsdata.Bda;this.Fa=this.getRoot().el().getAttribute("data-dccl")==="true"};_.A(WRc,_.mf);WRc.Ia=function(){return{jsdata:{Bda:_.NB}}};WRc.prototype.oa=function(){if(this.Fa)return!0;XRc(this);return!1};WRc.prototype.Ca=function(a){_.Qb(this.data,_.JB,14,a.data);XRc(this)};
var XRc=function(a){_.tu(a.getRoot().el());_.URc("fs");a.ka?_.lf(document,_.jjc,a.data.Qc()):_.lf(document,_.ijc,a.data);_.lf(window.document.body,_.Kwb);_.iw(a.getRoot().el(),"hide_popup");a.wa&&a.trigger(_.TRc)};_.G(WRc.prototype,"yM1YJe",function(){return this.Ca});_.G(WRc.prototype,"i5KCU",function(){return this.oa});_.ir(_.VRc,WRc);
_.z();
}catch(e){_._DumpException(e)}
try{
_.t5b=_.Bd("nabPbb",[]);
}catch(e){_._DumpException(e)}
try{
_.y("nabPbb");
var u5b=function(a){_.mf.call(this,a.Oa);this.ka=a.controller.Tk.Ma("xl07Ob").el();this.menu=_.co(a.controller.Tk,"xl07Ob");this.button=_.bo(a.controller.Tk,"LgbsSe");this.popup=a.controller.Tk;this.oa=_.Sf(this.getData("ffp"),!1)};_.A(u5b,_.mf);u5b.Ia=function(){return{controller:{Tk:"V68bde"}}};
u5b.prototype.Ca=function(a){var b=this,c=[];_.Xc(this.ka)&&c.push(new _.ln(this.ka,"show"));var d=a.data&&a.data.wc;d&&_.Xc(d)||(d=null);(d||c.length)&&_.qu(c,{wc:d||void 0});c=_.nl("searchform");d=this.popup.getPopup();c&&c.contains(a.targetElement.el())&&c.classList.contains("minidiv")?(_.sm.setStyle(c,"z-index",1E3),_.sm.setStyle(d,"position","fixed"),this.popup.QIa(0,_.Re().scrollY),this.popup.reposition()):this.oa&&(_.sm.setStyle(_.Du(),"z-index",2001),_.sm.setStyle(d,"position","fixed"),_.sm.setStyle(d,
"bottom",this.popup.Bp().getBoundingClientRect().height+"px"),_.sm.setStyle(d,"top",""));this.menu.then(function(e){if(e){e.getRoot().Ab().focus();for(var f=_.Na(e.Lta),g=f.next();!g.done;g=f.next()){g=g.value;var h=g.Vn();if(g.isEnabled()&&_.sm.Qh(h)){e.Tma(h);e.Na(h);break}}b.notify(_.l5b)}})};
u5b.prototype.wa=function(a){var b=_.nl("searchform"),c=this.popup.getPopup();b&&b.contains(a.targetElement.el())?(_.sm.setStyle(b,"z-index",""),_.sm.setStyle(c,"position",""),this.popup.QIa(0,0)):this.oa&&(_.sm.setStyle(_.Du(),"z-index",""),_.sm.setStyle(c,"position",""),_.sm.setStyle(c,"bottom",""))};u5b.prototype.Fa=function(){this.menu.then(function(a){a&&a.Tma(null)})};_.G(u5b.prototype,"VFzweb",function(){return this.Fa});_.G(u5b.prototype,"gDkf4c",function(){return this.wa});
_.G(u5b.prototype,"Y0y4c",function(){return this.Ca});_.ir(_.t5b,u5b);
_.z();
}catch(e){_._DumpException(e)}
})(this._hd);
// Google Inc.
