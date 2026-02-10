package com.recruitment.app.repository;

import com.recruitment.app.model.Application;
import com.recruitment.app.model.Job;
import com.recruitment.app.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ApplicationRepository extends JpaRepository<Application, Long> {
    // Find all applications for a specific job (Useful for HR)
    List<Application> findByJob(Job job);

    // Find all applications made by a specific user (Useful for Candidate Dashboard)
    List<Application> findByUser(User user);

    // Check if user already applied to avoid duplicates
    boolean existsByJobAndUser(Job job, User user);
}