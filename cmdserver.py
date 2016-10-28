import asyncio
import logging
# from config import led_stage, head_servo_stage, carve_servo_stage

from timerrr import timerrr


class cmd_server(asyncio.Protocol):

    def __init__(self, state):
        super().__init__()
        self.global_state = state

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log = logging.getLogger(
            'AlleyServer_{}_{}'.format(*self.address)
        )
        # self.log.debug('connection accepted')

    def data_received(self, data):
        # self.log.debug('received {}'.format(data))
        if data == b'PING':
            self.log.debug('Got PINGED!')
        elif data == b'MUSICSTART':
            print("Kicking off timer loops")
            asyncio.ensure_future(timerrr(self.global_state.loop))
        elif data == b'HEAD_NOD':
            #  self.log.debug('Changing head_servo_stage to NOD!')
            self.global_state.head_servo_stage = 'NOD'
        elif data == b'HEAD_TURN':
            #  self.log.debug('Changing head_servo_stage to TURN!')
            self.global_state.head_servo_stage = 'TURN'
        elif data == b'LED_STEADY':
            #  self.log.debug('Changing led_stage to SYNC!')
            self.global_state.led_stage = 'STEADY'
        elif data == b'LED_OFF':
            #  self.log.debug('Changing led_stage to SYNC!')
            self.global_state.led_stage = 'OFF'
        elif data == b'LED_SYNC':
            #  self.log.debug('Changing led_stage to SYNC!')
            self.global_state.led_stage = 'SYNC'
        elif data == b'LED_RAND':
            #  self.log.debug('Changing led_stage to STEADY!')
            self.global_state.led_stage = 'RAND'
        elif data == b'head_knife_round':
            print('Changing carve_stage to ROUND')
            self.global_state.carve_servo_stage = 'ROUND'
        elif data == b'head_knife_stab':
            print('Changing carve_stage to STAB!')
            self.global_state.carve_servo_stage = 'STAB'
        elif data == b'vines_still':
            print('Changing vines_stage to STILL!')
            self.global_state.vines_stage = 'STILL'
        elif data == b'vines_shake':
            print('Changing vines_stage to SHAKE')
            self.global_state.vines_stage = 'SHAKE'

    def eof_received(self):
        # self.log.debug('received EOF')
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, error):
        if error:
            self.log.error('ERROR: {}'.format(error))
        else:
            self.log.debug('closing')
        super().connection_lost(error)
