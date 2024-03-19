## Restaurant Database Overview

The Restaurant Database is a comprehensive solution designed to streamline restaurant management processes and enhance customer experiences. It comprises several interconnected tables tailored to meet the diverse needs of restaurant owners and managers:

### Tables and Columns:

- **Restaurant**:

  - **Columns**: `id` (primary key), `name`, `description`, `rating`, `telephone`, `hours`.
  - This table stores detailed information about restaurants, including their names, descriptions, ratings, contact telephone numbers, and operating hours. It serves as a centralized repository for restaurant data, facilitating easy access and management.

- **Address**:

  - **Columns**: `id` (primary key), `street_number`, `street_name`, `city`, `state`, `google_map_link`, `restaurant_id` (foreign key).
  - The Address table contains comprehensive address details for each restaurant, ensuring accurate location information. The `restaurant_id` column establishes a one-to-one relationship with the Restaurant table, enabling seamless navigation between addresses and their respective restaurants.

- **Category**:

  - **Columns**: `id` (primary key), `name`, `description`.
  - Categories represent different types of dishes offered by restaurants. This table allows restaurant owners to organize their menus efficiently, making it easier for customers to browse and select their desired dishes.

- **Dish**:

  - **Columns**: `id` (primary key), `name`, `description`, `hot_and_spicy`.
  - The Dish table contains detailed information about individual dishes served by restaurants. It includes attributes such as dish names, descriptions, and whether they are hot and spicy, providing valuable insights for both restaurant staff and customers.

- **Review**:

  - **Columns**: `id` (primary key), `rating`, `description`, `date`, `restaurant_id` (foreign key).
  - Reviews of restaurants are stored in this table, enabling customers to share their feedback and experiences. The `restaurant_id` column establishes a one-to-many relationship with the Restaurant table, allowing reviews to be associated with specific restaurants.

- **Categories_Dishes**:
  - **Columns**: `category_id` (foreign key), `dish_id` (foreign key), `price`.
  - This junction table facilitates many-to-many relationships between categories and dishes. It allows restaurant owners to assign multiple dishes to various categories while providing flexibility in pricing.

### Purpose and Benefits:

The Restaurant Database aims to empower restaurant owners and managers with a centralized platform to efficiently manage their establishments and enhance customer satisfaction. Its key purposes and benefits include:

- **Menu Management**: The database enables restaurant owners to create and update menus seamlessly, categorizing dishes and setting prices with ease.

- **Location Accuracy**: Accurate address information ensures that customers can easily locate and navigate to restaurants, enhancing convenience and accessibility.

- **Customer Feedback**: By storing reviews and ratings, the database enables restaurants to gather valuable feedback from customers, helping them identify areas for improvement and maintain service quality.

- **Operational Efficiency**: With comprehensive data storage and streamlined management processes, the database promotes operational efficiency, allowing restaurant staff to focus on delivering exceptional dining experiences.

- **Data-Driven Decision Making**: Access to detailed insights and analytics derived from the database empowers restaurant owners to make informed decisions, optimize menus, and tailor services to meet customer preferences.

### Database Diagram

![Database Diagram](/projects/build-a-menu-database/menu-database-diagram.png "Database Diagram")
