package com.recruitment.app.repository;

import com.recruitment.app.model.Job;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;

public interface JobRepository extends JpaRepository<Job, Long> {

    // --- CRITICAL FIX: Must return List<Job>, not just Job ---
    List<Job> findByPostedById(Long userId);
    // --------------------------------------------------------

    // Your existing search query
    @Query("SELECT j FROM Job j WHERE " +
            "(:keyword IS NULL OR :keyword = '' OR LOWER(j.title) LIKE LOWER(CONCAT('%', :keyword, '%'))) AND " +
            "(:location IS NULL OR :location = '' OR :location = 'All Locations' OR j.location = :location)")
    List<Job> searchJobs(@Param("keyword") String keyword, @Param("location") String location);
}