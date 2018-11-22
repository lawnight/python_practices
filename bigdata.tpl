package com.digisky.gal.warstates.gameserver.bigdata.logs;

import com.digisky.gal.warstates.gameserver.bigdata.model.AbstractBigdataLog;
import com.digisky.gal.warstates.gameserver.config.GameServerConfig;
import com.digisky.gal.warstates.gameserver.module.player.service.Player;
import com.digisky.gal.warstates.gameserver.utils.log.MessageFormatUtils;
import name.skycat.game.common.utils.lang.StringConstants;

/**
 * $des
 *  created by tools
 * @author: lijiangtao
 * @email: near.li@qq.com
 * @create: 2018-11-22 15:38
 **/
public class $classLog extends AbstractBigdataLog {
    /** 日志名称 */
    private static final String NAME = "$class";
    /** 序列化格式 */
    private static final String FORMAT_PATTERN = "$fields_format";
    $fields_fcc

    /**
     * 构造方法
     *
     * @param player       玩家实体
     * @param serverConfig 服务器配置
     */
    public $classLog(Player player, GameServerConfig serverConfig) {
        super(player, serverConfig);
        this.serverId = String.valueOf(serverConfig.getServerId());
    }

    @Override
    public String format() {
        return MessageFormatUtils.format(FORMAT_PATTERN, NAME, $fields_com);
    }
}
