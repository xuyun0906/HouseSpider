create table xiaoqu_list(
id varchar(255) default  null comment '小区ID' ,
name varchar(255)default  null comment '小区名字',
huxingCount  varchar(40) default null comment '户型数',
chengjiaoCount varchar(40) default null comment '历史成交套数',
zaizuCount varchar(40)  default null comment '在租套数',
zaishouCount varchar(40)  default null comment '在售套数',
avgPrice varchar(40)   default null comment '均价',
region varchar(40)   default null comment '区域-行政区',
district varchar(40) default null comment '二级区域',
city varchar(20) default null comment '城市',
createTime timestamp default CURRENT_TIMESTAMP comment '创建时间'
);

create table xiaoqu_detail(
id varchar(255) default  null comment '小区ID',
name varchar(255)default  null comment '小区名字',
buildYear  varchar(40) default null  comment '建筑年代',
bulidType varchar(60)  default null  comment '建筑类型',
wuyeFee varchar(80)  default null  comment '物业费用',
wuyeCompany varchar(255) default null  comment '物业公司',
developers varchar(255) default null  comment '开发商',
loudongCount varchar(80) default null  comment '楼栋总数',
fangwuCount varchar(80) default null  comment '房屋总数',
createTime timestamp default CURRENT_TIMESTAMP comment '创建时间'
);

create table house_list(
name varchar(500)default  null comment '小区名字',
city varchar(20) default null comment '城市',
xiaoquId   varchar(255) default  null comment '小区ID',
xiaoquName  varchar(255) default  null comment '小区名字',
mianJi varchar(60)  default null comment '面积',
floor varchar(80)  default null comment '楼层',
huXing varchar(80)  default null comment '户型',
totalPrice varchar(80) default null comment '总价',
price  varchar(80) default null comment '单价',
direct varchar(40)  default null comment '朝向',
fitment varchar(80) default null comment '装修',
lift  varchar(80) default null comment '电梯',
buildType varchar(100) default null comment '建筑类型',
district varchar(40) default null comment '二级区域',
createTime timestamp default CURRENT_TIMESTAMP comment '创建时间'
);


