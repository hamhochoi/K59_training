 import java.util.Properties;

import javax.naming.Context;
import javax.naming.InitialContext;

import javax.jms.Queue;
import javax.jms.Session;
import javax.jms.TextMessage;
import javax.jms.QueueSender;
import javax.jms.DeliveryMode;
import javax.jms.QueueSession;
import javax.jms.QueueConnection;
import javax.jms.QueueConnectionFactory;

public class pulisher {

	public static void main(String[] args) throws Exception {
		Properties env = new Properties();
		env.put(Context.INITIAL_CONTEXT_FACTORY,
				"org.apache.activemq.jndi.ActiveMQInitialContextFactory");
		env.put(Context.PROVIDER_URL, "tcp://localhost:61616");
		env.put("queue.queueSampleQueue", "MyNewQueue");
		InitialContext ctx = new InitialContext(env);

		//tìm đối tg hành đợi
		Queue queue = (Queue) ctx.lookup("queueSampleQueue");
		//tìm kiếm factory
		QueueConnectionFactory connFactory = (QueueConnectionFactory) ctx.lookup("QueueConnectionFactory");
		//tạo trùy cập hàng đợi
		QueueConnection queueConn = connFactory.createQueueConnection();

		//tạo phiên làm việc
		QueueSession queueSession = queueConn.createQueueSession(false,Session.DUPS_OK_ACKNOWLEDGE);

		//Gửi
		QueueSender queueSender = queueSession.createSender(queue);
		queueSender.setDeliveryMode(DeliveryMode.NON_PERSISTENT);

		//ví dụ lời nhắn
		TextMessage message = queueSession.createTextMessage(" hihiii");

		//bắt đầu gửi đi
		queueSender.send(message);

		System.out.println("sent: " + message.getText());

		queueConn.close();
	}
}