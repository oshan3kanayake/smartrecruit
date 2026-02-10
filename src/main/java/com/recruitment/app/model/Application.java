package com.recruitment.app.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "applications")
public class Application {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Which Job is this for?
    @ManyToOne
    @JoinColumn(name = "job_id", nullable = false)
    private Job job;

    // Which User applied?
    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    private String status; // e.g., "Pending", "Accepted", "Rejected"

    private LocalDateTime appliedAt;

    // --- NEW: For Resume Upload ---
    private String resumeFileName;

    // CONSTRUCTOR
    public Application() {
        this.appliedAt = LocalDateTime.now();
        this.status = "Pending";
    }

    // GETTERS AND SETTERS
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Job getJob() { return job; }
    public void setJob(Job job) { this.job = job; }

    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public LocalDateTime getAppliedAt() { return appliedAt; }
    public void setAppliedAt(LocalDateTime appliedAt) { this.appliedAt = appliedAt; }

    public String getResumeFileName() { return resumeFileName; }
    public void setResumeFileName(String resumeFileName) { this.resumeFileName = resumeFileName; }

    // ... inside Application class ...

    @Transient // This means "Don't save this to the database, just use it for now"
    private int transientScore;

    public int getTransientScore() { return transientScore; }
    public void setTransientScore(int transientScore) { this.transientScore = transientScore; }

// ... rest of class ...
}