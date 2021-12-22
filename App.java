package org.neo4j.driver;

import org.neo4j.driver.*;

public class App {
    public static void main(String[] args) {
        final Driver driver;
        try {
            driver = GraphDatabase.driver("bolt://localhost:7687", AuthTokens.basic("neo4j", "1234"),
                    Config.builder().build());
            driver.session(SessionConfig.forDatabase("LAB1_1"));


            final String query = "CREATE (RVacuum:Vacuum {title: \"Samsung\" })\n" +
                    "CREATE (Smartphone:Smartphone {title: \"Samsung\" })\n" +
                    "CREATE (ChargingDevice:ChargingDevice {title:\"Charging Device\", type: \"Автоматическая зарядка\" })\n" +
                    "\n" +
                    "CREATE (Cleaning:BasicFunction {title:\"Cleaning\", type: \"Сухая\" }) \n" +
                    "CREATE (LC:AdditionalFunction {title:\"Ароматизация помещения\"})\n" +
                    "CREATE (CTC:AdditionalFunction {title:\"Ограничение времени уборки\"})\n" +
                    "CREATE (RVacuum) - [:hasFunction {title:\"имеет функцию\"}] -> (Cleaning)\n" +
                    "CREATE (RVacuum) - [:hasFunction {title:\"имеет функцию\"}] -> (LC)\n" +
                    "CREATE (RVacuum) - [:hasFunction {title:\"имеет функцию\"}] -> (CTC)\n" +
                    "\n" +
                    "CREATE (Component:Component {title:\"Sensor\", type: \"Инфракрасная\" })\n" +
                    "CREATE (RVacuum) - [:hasComponent {title:\"имеет компонент\"}] -> (Component)\n" +
                    "\n" +
                    "CREATE (RVacuum) - [:canBeControlledWith {title:\"управляется с помощью\"}] -> (Smartphone)\n" +
                    "\n" +
                    "CREATE (RVacuum) - [:chargesWith  {title:\"заряжается с помощью\"}] -> (ChargingDevice)";

            try (Session session = driver.session()) {
                String add = session.writeTransaction(new TransactionWork<String>() {
                    @Override
                    public String execute(Transaction tx) {
                        Result result = tx.run(query);
                        return result.toString();
                    }
                });
                System.out.println("Данные добавлены.");
            }

            driver.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
