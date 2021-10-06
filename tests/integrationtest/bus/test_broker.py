from energytt_platform.bus import MessageBroker, Message


class TestMessageBroker:
    """
    TODO
    """

    def test__poll__publish_message_to_topic__should_receive_dict_of_messages(
            self,
            broker: MessageBroker,
            msg1: Message,
            msg2: Message,
    ):
        """
        TODO
        """

        # -- Act -------------------------------------------------------------

        broker.publish(topic='TOPIC1', msg=msg1)
        broker.publish(topic='TOPIC2', msg=msg2)

        broker.subscribe(['TOPIC1', 'TOPIC2'])

        received_messages = broker.poll(timeout=5)

        # -- Assert ----------------------------------------------------------

        assert received_messages == {
            'TOPIC1': [msg1],
            'TOPIC2': [msg2],
        }

    def test__poll_list__publish_message_to_topic__should_receive_message_in_list(
            self,
            broker: MessageBroker,
            msg1: Message,
    ):
        """
        TODO
        """

        # -- Act -------------------------------------------------------------

        broker.publish(topic='TOPIC1', msg=msg1)

        broker.subscribe(['TOPIC1'])

        received_messages = broker.poll_list(timeout=5)

        # -- Assert ----------------------------------------------------------

        assert received_messages == [msg1]
