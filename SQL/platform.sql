/*
Navicat MySQL Data Transfer

Source Server         : 192.168.38.129
Source Server Version : 50173
Source Host           : 192.168.38.129:3306
Source Database       : platform

Target Server Type    : MYSQL
Target Server Version : 50173
File Encoding         : 65001

Date: 2016-04-06 14:03:44
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `platuser`
-- ----------------------------
DROP TABLE IF EXISTS `platuser`;
CREATE TABLE `platuser` (
  `user_id` char(20) NOT NULL DEFAULT '',
  `user_name` char(20) DEFAULT NULL,
  `user_pwd` char(32) DEFAULT NULL,
  `user_level` int(2) DEFAULT NULL,
  `user_part` char(20) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of platuser
-- ----------------------------

-- ----------------------------
-- Table structure for `status_items`
-- ----------------------------
DROP TABLE IF EXISTS `status_items`;
CREATE TABLE `status_items` (
  `items` char(30) NOT NULL COMMENT '检查项'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of status_items
-- ----------------------------

-- ----------------------------
-- Table structure for `status_items_20160315`
-- ----------------------------
DROP TABLE IF EXISTS `status_items_20160315`;
CREATE TABLE `status_items_20160315` (
  `items` char(30) NOT NULL COMMENT '检查项'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of status_items_20160315
-- ----------------------------

-- ----------------------------
-- Table structure for `tb_daily_data`
-- ----------------------------
DROP TABLE IF EXISTS `tb_daily_data`;
CREATE TABLE `tb_daily_data` (
  `id` int(11) NOT NULL DEFAULT '0',
  `nums` int(6) NOT NULL DEFAULT '0',
  `content` char(40) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tb_daily_data
-- ----------------------------

-- ----------------------------
-- Table structure for `tb_item_code`
-- ----------------------------
DROP TABLE IF EXISTS `tb_item_code`;
CREATE TABLE `tb_item_code` (
  `item_id` int(4) NOT NULL DEFAULT '0',
  `item_name` char(30) DEFAULT NULL,
  `range_begin` int(5) DEFAULT NULL,
  `steps` int(4) DEFAULT '1',
  PRIMARY KEY (`item_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tb_item_code
-- ----------------------------
